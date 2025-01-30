package main

import (
	"archive/tar"
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"strconv"
	"strings"
	"time"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/client"
)

// TestCase tuzilmasi
type TestCase struct {
	TestCase       int     `json:"test_case"`
	Input          []int   `json:"input"`
	ExpectedOutput int     `json:"expected_output"`
	ActualOutput   int     `json:"actual_output"`
	Passed         bool    `json:"passed"`
	Language       string  `json:"language"`
	CPUUsage       float64 `json:"cpu_usage"`
	MemoryUsage    uint64  `json:"memory_usage"`
	ExecutionTime  string  `json:"execution_time"`
}

func createTarFile(fileName, content string) (*bytes.Buffer, error) {
	buffer := new(bytes.Buffer)
	tarWriter := tar.NewWriter(buffer)
	defer tarWriter.Close()

	hdr := &tar.Header{
		Name: fileName,
		Mode: 0600,
		Size: int64(len(content)),
	}
	if err := tarWriter.WriteHeader(hdr); err != nil {
		return nil, fmt.Errorf("Tar header yozishda xatolik: %v", err)
	}
	if _, err := tarWriter.Write([]byte(content)); err != nil {
		return nil, fmt.Errorf("Tar fayl yozishda xatolik: %v", err)
	}

	return buffer, nil
}

func getContainerStats(cli *client.Client, containerName string) (float64, uint64, error) {
	stats, err := cli.ContainerStatsOneShot(context.Background(), containerName)
	if err != nil {
		return 0, 0, fmt.Errorf("Konteyner statistikasi olishda xatolik: %v", err)
	}
	defer stats.Body.Close()

	var statsJSON types.StatsJSON
	if err := json.NewDecoder(stats.Body).Decode(&statsJSON); err != nil {
		return 0, 0, fmt.Errorf("Statistikani o'qishda xatolik: %v", err)
	}

	cpuDelta := float64(statsJSON.CPUStats.CPUUsage.TotalUsage - statsJSON.PreCPUStats.CPUUsage.TotalUsage)
	systemDelta := float64(statsJSON.CPUStats.SystemUsage - statsJSON.PreCPUStats.SystemUsage)
	cpuUsage := (cpuDelta / systemDelta) * float64(len(statsJSON.CPUStats.CPUUsage.PercpuUsage)) * 100.0

	memoryUsage := statsJSON.MemoryStats.Usage

	return cpuUsage, memoryUsage, nil
}

func codeRunIn(cli *client.Client, containerName, language, fileName, input string) (string, error) {
	var cmd string
	switch language {
	case "python":
		cmd = fmt.Sprintf("python /app/%s", fileName)
	case "go":
		cmd = fmt.Sprintf("go run /app/%s", fileName)
	case "java":
		cmd = fmt.Sprintf("javac /app/%s && java -cp /app Solution", fileName)
	case "cpp":
		cmd = fmt.Sprintf("g++ /app/%s -o /app/output && /app/output", fileName)
	case "javascript":
		cmd = fmt.Sprintf("node /app/%s", fileName)
	default:
		return "", fmt.Errorf("Qo'llab-quvvatlanmaydigan dasturlash tili")
	}

	execConfig := types.ExecConfig{
		AttachStdout: true,
		AttachStderr: true,
		AttachStdin:  true,
		Cmd:          []string{"sh", "-c", cmd},
		Tty:          false,
	}

	execIDResp, err := cli.ContainerExecCreate(context.Background(), containerName, execConfig)
	if err != nil {
		return "", fmt.Errorf("Exec yaratishda xatolik: %v", err)
	}

	resp, err := cli.ContainerExecAttach(context.Background(), execIDResp.ID, types.ExecStartCheck{})
	if err != nil {
		return "", fmt.Errorf("Exec boshlashda xatolik: %v", err)
	}
	defer resp.Close()

	// Input uzatish
	if _, err := resp.Conn.Write([]byte(input + "\n")); err != nil {
		return "", fmt.Errorf("Input uzatishda xatolik: %v", err)
	}

	var output strings.Builder
	if _, err := io.Copy(&output, resp.Reader); err != nil {
		return "", fmt.Errorf("Chiqishni o'qishda xatolik: %v", err)
	}

	return strings.TrimSpace(output.String()), nil
}

func main() {
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		fmt.Printf("Docker client yaratishda xatolik: %v\n", err)
		return
	}
	defer cli.Close()

	var language string
	fmt.Print("Dasturlash tilini kiriting (python, go, java, cpp, javascript): ")
	fmt.Scanln(&language)

	var containerName string
	switch language {
	case "python":
		containerName = "python-app"
	case "go":
		containerName = "go-app"
	case "java":
		containerName = "java-app"
	case "cpp":
		containerName = "cpp-app"
	case "javascript":
		containerName = "js-app"
	default:
		fmt.Println("Qo'llab-quvvatlanmaydigan dasturlash tili.")
		return
	}

	testCases := []TestCase{
		{TestCase: 1, Input: []int{3, 5}, ExpectedOutput: 8, Language: language},
		{TestCase: 2, Input: []int{-1, 1}, ExpectedOutput: 0, Language: language},
	}

	for i, testCase := range testCases {
		inputStr := fmt.Sprintf("%d,%d", testCase.Input[0], testCase.Input[1])
		startTime := time.Now()

		output, err := codeRunIn(cli, containerName, language, "solution", inputStr)
		if err != nil {
			fmt.Printf("TestCase %d xato: %v\n", i+1, err)
			continue
		}

		cpuUsage, memoryUsage, err := getContainerStats(cli, containerName)
		if err != nil {
			fmt.Printf("Statistika olishda xatolik: %v\n", err)
			continue
		}

		elapsedTime := time.Since(startTime)
		actualOutput, _ := strconv.Atoi(output)
		passed := actualOutput == testCase.ExpectedOutput

		testCase.ActualOutput = actualOutput
		testCase.Passed = passed
		testCase.CPUUsage = cpuUsage
		testCase.MemoryUsage = memoryUsage
		testCase.ExecutionTime = elapsedTime.String()

		result, _ := json.MarshalIndent(testCase, "", "  ")
		fmt.Println(string(result))
	}
}

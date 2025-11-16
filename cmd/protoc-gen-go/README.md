# 快速使用（Windows）

仅保留两条核心命令：编译生成 exe 和将 proto 转换为 Go。

## 1. 编译生成 exe

```powershell
go build -o .\protoc-gen-go.exe .
```

## 2. proto 转换为 Go

示例使用仓库内的简单测试文件：`testdata\simple\hello.proto`

```powershell
protoc --plugin=protoc-gen-go="protoc-gen-go.exe" --go_out=./out --go_opt=paths=source_relative -I .\testdata\custom_tags\ tags.proto
```

说明：

- 请确保已安装 `protoc` 并可在命令行使用（`protoc --version`）。
- 若已将 `protoc-gen-go.exe` 加入 `PATH`，可省略 `--plugin=...`。

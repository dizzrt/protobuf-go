#!/usr/bin/env python3
"""
protoc代码生成Python脚本
基于之前讨论的路径问题解决方案，提供健壮的Python实现
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, List


def generate_go_code(
    proto_file: str,
    plugin_exe: str = "protoc-gen-go.exe",
    output_dir: str = "./testdata/custom_tags/",
    include_dirs: Optional[List[str]] = None,
) -> bool:
    """
    使用protoc生成Go代码

    Args:
        proto_file: proto文件路径
        plugin_exe: protoc-gen-go插件路径
        output_dir: 输出目录路径
        include_dirs: 包含目录列表，默认为None时使用output_dir

    Returns:
        bool: 执行是否成功
    """

    # 设置默认包含目录
    if include_dirs is None:
        include_dirs = [output_dir]

    try:
        if not os.path.isfile(plugin_exe):
            print(f"错误: 插件文件 '{plugin_exe}' 不存在")
            return False

        # 构建protoc命令参数
        cmd_args = [
            "protoc",
            f"--plugin=protoc-gen-go={plugin_exe}",
            f"--go_out={output_dir}",
            "--go_opt=paths=source_relative",
        ]

        # 添加包含目录参数
        for include_dir in include_dirs:
            cmd_args.append(f"-I")
            cmd_args.append(include_dir)

        # 添加proto文件
        cmd_args.append(proto_file)

        # 打印执行信息
        print(f"正在生成Go代码...")
        print(f"Proto文件: {proto_file}")
        print(f"插件: {plugin_exe}")
        print(f"输出目录: {output_dir}")
        print(f"包含目录: {include_dirs}")
        print(f"执行命令: {' '.join(cmd_args)}")

        # 执行protoc命令
        result = subprocess.run(cmd_args, capture_output=True, text=True, check=False)

        # 检查执行结果
        if result.returncode == 0:
            print(f"✓ 代码生成成功！")
            return True
        else:
            print(f"✗ 代码生成失败")
            print(f"错误输出: {result.stderr}")
            return False

    except FileNotFoundError:
        print("错误: protoc命令未找到，请先安装protobuf")
        return False
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        return False


def batch_generate_go_code(
    proto_files: List[str],
    plugin_exe: str = "protoc-gen-go.exe",
    output_dir: str = "./testdata/custom_tags/",
    include_dirs: Optional[List[str]] = None,
) -> List[str]:
    """
    批量生成多个proto文件的Go代码

    Args:
        proto_files: proto文件路径列表
        plugin_exe: protoc-gen-go插件路径
        output_dir: 输出目录路径
        include_dirs: 包含目录列表

    Returns:
        List[str]: 成功生成的文件列表
    """
    successful_files = []

    for proto_file in proto_files:
        print(f"\n处理文件: {proto_file}")
        if generate_go_code(proto_file, plugin_exe, output_dir, include_dirs):
            successful_files.append(proto_file)

    return successful_files


def find_proto_files(directory: str) -> List[str]:
    """
    在指定目录中查找所有proto文件

    Args:
        directory: 搜索目录

    Returns:
        List[str]: proto文件路径列表
    """
    proto_files = []
    dir_path = Path(directory)

    if dir_path.exists() and dir_path.is_dir():
        for proto_file in dir_path.glob("**/*.proto"):
            proto_files.append(str(proto_file))

    return proto_files


# 使用示例
if __name__ == "__main__":
    print("\n=== 批量生成测试 ===")
    all_proto_files = find_proto_files("./testdata/custom_tags/")

    if all_proto_files:
        successful = batch_generate_go_code(
            proto_files=all_proto_files,
            plugin_exe="protoc-gen-go.exe",
            output_dir="./testdata/custom_tags/",
        )
        print(f"\n批量生成完成，成功处理 {len(successful)} 个文件")
    else:
        print("未找到proto文件")

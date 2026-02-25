# Makefile for Deepseek API Client

# 编译器设置
CC = gcc
OBJC = gcc
CFLAGS = -Wall -Wextra -Iinclude
OBJCFLAGS = -Wall -Wextra -Iinclude -framework Cocoa -framework Foundation -framework AppKit
LDFLAGS = -lcurl

# 目标文件
TARGET = deepseek-api-gui

# 源文件
C_SOURCES = src/api_client.c src/session.c src/chat_history.c src/config.c
OBJC_SOURCES = src/main.m

# 目标文件
OBJECTS = $(C_SOURCES:.c=.o) $(OBJC_SOURCES:.m=.o)

# 默认目标
all: $(TARGET)

# 编译目标
$(TARGET): $(OBJECTS)
	$(OBJC) $(OBJCFLAGS) $(LDFLAGS) -o $(TARGET) $(OBJECTS)

# 编译C文件
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# 编译Objective-C文件
%.o: %.m
	$(OBJC) $(OBJCFLAGS) -c $< -o $@

# 清理
clean:
	rm -f $(OBJECTS) $(TARGET) $(CLI_OBJECTS) $(CLI_TARGET)

# 终端版本目标
CLI_TARGET = deepseek-api

# 终端版本源文件
CLI_SOURCES = src/cli_main.c src/api_client.c src/session.c src/chat_history.c src/config.c

# 终端版本目标文件
CLI_OBJECTS = $(CLI_SOURCES:.c=.o)

# 编译终端版本
cli: $(CLI_TARGET)

# 终端版本编译规则
$(CLI_TARGET): $(CLI_OBJECTS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(CLI_TARGET) $(CLI_OBJECTS)

# 运行终端版本
run_cli: $(CLI_TARGET)
	./$(CLI_TARGET)

# 运行GUI版本
run: $(TARGET)
	./$(TARGET)

# 运行Python终端版本
run_py_cli:
	python3 src/cli_main.py

# 运行Python GUI版本
run_py_gui:
	python3 src/gui_main.py

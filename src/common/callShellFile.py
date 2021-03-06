#!/usr/bin/python3
# coding=utf-8

import os
import subprocess
import time

from common.logger import Logger

proDir = os.path.split(os.path.realpath(__file__))[0]
shell_file_path = os.path.join(proDir, "../shellFile/")
source_file_path = os.path.join(proDir, "../source/")


class CallShell:
    def __init__(self):
        self.log = Logger()
        self.input_file = os.path.join(source_file_path, "sample.mp4")
        self.ffmpeg_file = os.path.join(shell_file_path, "ffmpeg_stream.sh")
        self.re_orc_file = os.path.join(shell_file_path, "restart_orc.sh")
        self.re_omp_file_different = os.path.join(shell_file_path, "restart_omp_different.sh")
        self.re_omp_file_same = os.path.join(shell_file_path, "restart_omp_same.sh")
        self.start_omp_file = os.path.join(shell_file_path, "start_omp.sh")
        self.stop_omp_file = os.path.join(shell_file_path, "stop_omp.sh")
        self.cre_test_file = os.path.join(shell_file_path, "create_test_file.sh")

    def call_ffmpeg(self, stream_link):
        """Live channel推流
        :param stream_link: 推流地址
        :return:
        """
        # 开始推流
        try:
            self.log.warning(message="开始推流>>>")
            print(self.ffmpeg_file)
            print(self.input_file)
            process = subprocess.Popen(args=[self.ffmpeg_file, self.input_file, stream_link])
            # 等待30秒,待推流结束
            self.log.warning(message="正在推流...")
            time.sleep(30)
        except Exception as e:
            self.log.error(message="Live Channel推流过程中，执行脚本遇到错误: %s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="推流结束...")
            self.log.warning(message="推流程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭推流程序错误：%s" % e)

    def call_restart_orc(self):
        # 重启orc
        try:
            self.log.warning(message="ORC重启>>>")
            process = subprocess.Popen(args=[self.re_orc_file])
            # 等待5秒，待orc重启完成
            self.log.warning(message="ORC正在重启...")
            time.sleep(5)
        except Exception as e:
            self.log.error(message="执行重启ORC脚本遇到错误：%s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="ORC重启完成!!")
            self.log.warning(message="重启程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭重启程序错误：%s" % e)

    def call_restart_omp_different(self):
        # 重启omp
        try:
            self.log.warning(message="OMP重启>>>")
            process = subprocess.Popen(args=[self.re_omp_file_different])
            # 等待35秒，待omp重启完成
            self.log.warning(message="OMP正在重启，请稍后...")
            time.sleep(35)
        except Exception as e:
            self.log.error(message="执行重启OMP脚本遇到错误：%s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="OMP重启完成!!")
            self.log.warning(message="重启程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭重启程序错误：%s" % e)

    def call_restart_omp_same(self):
        # 重启omp
        try:
            self.log.warning(message="OMP重启>>>")
            process = subprocess.Popen(args=[self.re_omp_file_same])
            # 等待35秒，待omp重启完成
            self.log.warning(message="OMP正在重启，请稍后...")
            time.sleep(35)
        except Exception as e:
            self.log.error(message="执行重启OMP脚本遇到错误：%s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="OMP重启完成!!")
            self.log.warning(message="重启程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭重启程序错误：%s" % e)

    def call_start_omp(self):
        # 启动omp
        try:
            self.log.warning(message="OMP启动>>>")
            process = subprocess.Popen(args=[self.start_omp_file])
            # 等待35秒，待omp完成启动
            self.log.warning(message="OMP正在启动，请稍后...")
            time.sleep(35)
        except Exception as e:
            self.log.error(message="执行启动OMP脚本遇到错误：%s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="OMP重启完成!!")
            self.log.warning(message="重启程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭重启程序错误：%s" % e)

    def call_stop_omp(self):
        # 停止omp
        try:
            self.log.warning(message="OMP停止>>>")
            process = subprocess.Popen(args=[self.stop_omp_file])
            # 等待5秒，待omp停止
            self.log.warning(message="OMP正在停止，请稍后...")
            time.sleep(5)
        except Exception as e:
            self.log.error(message="执行停止OMP脚本遇到错误：%s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="OMP已经停止!!")
            self.log.warning(message="停止程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭停止程序错误：%s" % e)

    def call_create_test_file(self):
        # 创建测试文件
        try:
            self.log.warning(message="创建测试相关目录及文件>>>")
            process = subprocess.Popen(args=[self.cre_test_file])
            # 等待5秒
            self.log.warning(message="测试文件及目录正在创建，请稍后...")
            time.sleep(5)
        except Exception as e:
            self.log.error(message="执行停止创建文件目录脚本遇到错误：%s" % e)

        # 关闭推流进程程序
        try:
            process.terminate()
            self.log.warning(message="测试文件及目录已经创建成功!!")
            self.log.warning(message="创建程序已关闭!!!")
        except Exception as e:
            self.log.error(message="关闭创建程序错误：%s" % e)


if __name__ == '__main__':
    stream_link = "rtmp://172.16.1.201:44437/live/5d3ea109731cba080b5f7ec7"
    call = CallShell()
    # call.call_create_test_file()
    call.call_ffmpeg(stream_link)

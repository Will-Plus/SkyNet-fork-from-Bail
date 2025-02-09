#SkyNet  Word out-of-order processor
#单词乱序处理器 3.0
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random

class SNFShufflerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkyNet单词乱序处理器")
        self.geometry("400x136")
        self.output_dir = "Word out-of-order"
        
        # 初始化数据结构
        self.file_header = []
        self.word_list = []
        self.current_file = ""
        
        # 创建界面
        self.create_widgets()
        self.check_output_dir()

    def create_widgets(self):
        # 文件选择区域
        file_frame = tk.Frame(self)
        file_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.btn_select = tk.Button(
            file_frame,
            text="选择课程文件",
            command=self.load_snf_file,
            width=10
        )
        self.btn_select.pack(side=tk.LEFT)
        
        self.lbl_file = tk.Label(file_frame, text="未选择文件", width=50 , anchor='w')
        self.lbl_file.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 处理按钮
        self.btn_process = tk.Button(
            self,
            text="处理并导出乱序文件",
            command=self.process_and_export,
            state=tk.DISABLED
        )
        self.btn_process.pack(pady=10)
        
        # 状态栏
        self.status = tk.Label(self, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def check_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            self.update_status(f"已创建输出目录: {self.output_dir}")

    def load_snf_file(self):
        filetypes = [(".snf文件", "*.snf"), ("所有文件", "*.*")]
        file_path = filedialog.askopenfilename(title="选择课程文件", filetypes=filetypes)
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 读取前两行作为头部
                    self.file_header = [next(f) for _ in range(2)]
                    
                    # 处理剩余行
                    self.word_list = []
                    for line in f:
                        line = line.strip()
                        if line:
                            # 支持多种分隔符
                            if '\t' in line:
                                parts = line.split('\t', 1)
                            elif '|' in line:
                                parts = line.split('|', 1)
                            else:
                                parts = line.split(' ', 1)
                            
                            word = parts[0].strip()
                            definition = parts[1].strip() if len(parts) > 1 else ""
                            self.word_list.append((word, definition))
                
                self.current_file = file_path
                self.lbl_file.config(text=os.path.basename(file_path))
                self.btn_process.config(state=tk.NORMAL)
                self.update_status(f"已加载文件: {len(self.word_list)} 个单词")
                
            except Exception as e:
                messagebox.showerror("错误", f"文件读取失败: {str(e)}")
                self.reset_state()

    def process_and_export(self):
        try:
            # 打乱单词列表
            shuffled = self.word_list.copy()
            random.shuffle(shuffled)
            
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            output_name = f"{base_name} Out order.snf"
            output_path = os.path.join(self.output_dir, output_name)
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                # 写入原始头部
                f.writelines(self.file_header)
                # 写入乱序数据
                for word, definition in shuffled:
                    f.write(f"{word}\t{definition}\n")
            
            # 显示结果
            success_msg = (
                f"成功处理 {len(shuffled)} 个单词！\n"
                f"输出文件: {output_path}"
            )
            messagebox.showinfo("处理完成", success_msg)
            self.update_status(f"已导出: {output_name}")
            
            # 打开输出目录（Windows系统）
            if os.name == 'nt':
                os.startfile(self.output_dir)
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.update_status("导出失败")

    def update_status(self, message):
        self.status.config(text=message)
        self.update_idletasks()

    def reset_state(self):
        self.file_header = []
        self.word_list = []
        self.current_file = ""
        self.lbl_file.config(text="未选择文件")
        self.btn_process.config(state=tk.DISABLED)
        self.update_status("就绪")

if __name__ == "__main__":
    app = SNFShufflerApp()
    app.mainloop()
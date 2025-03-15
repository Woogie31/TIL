import tkinter as tk
from tkinter import messagebox
import pyautogui  # 매크로용 라이브러리
import time
import threading

class SimpleApp:

    count = 0

    def __init__(self):
        # 메인 윈도우 생성
        self.window = tk.Tk()
        self.window.title("Custom UI Program")
        self.window.geometry("300x200")  # 창 크기 변경
        
        # 매크로 상태 변수 추가 
        self.is_macro_running = False
        self.macro_thread = None  # 스레드 변수 추가
        
        # 창 배경색 설정
        self.window.configure(bg='#f0f0f0')  # 배경색 설정
        
        # 버튼들을 담을 프레임
        self.button_frame = tk.Frame(
            self.window,
            bg='#f0f0f0',
            padx=20,  # 좌우 여백
            pady=20   # 상하 여백
        )
        self.button_frame.pack(expand=True)
        
        # 시작작 버튼 - 모던한 스타일
        self.macro_button = tk.Button(
            self.button_frame,
            text="매크로 시작",
            command=self.toggle_macro,
            bg='lightgreen',
            font=('Arial', 12)
        )
        
        self.macro_button.pack(side=tk.LEFT, padx=10)

        # 종료 버튼 - 기본 스타일에 커스텀 색상
        self.exit_button = tk.Button(
            self.button_frame,
            text="종료",
            command=self.quit_program,
            bg='#ff6b6b',  # 배경색
            fg='white',    # 글자색
            font=('맑은 고딕', 12),
            relief='flat',  # 버튼 테두리 스타일
            cursor='hand2'  # 마우스 오버 시 커서 모양
        )
        self.exit_button.pack(side=tk.LEFT, padx=10)
        
        # 버튼에 마우스 오버 효과 추가
        for button in [self.exit_button, self.macro_button]:
            button.bind('<Enter>', self.on_enter)
            button.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        event.widget['bg'] = '#ff5252'

    def on_leave(self, event):
        event.widget['bg'] = '#ff6b6b'
        
    def toggle_macro(self):
        if not self.is_macro_running:
            self.is_macro_running = True
            self.macro_button.config(text="매크로 정지", bg='pink')
            # 새로운 스레드에서 매크로 실행
            self.macro_thread = threading.Thread(target=self.run_macro)
            self.macro_thread.daemon = True # 메인 프로그램 종료시 스레드도 종료
            self.macro_thread.start()
        else:
            self.is_macro_running = False
            self.macro_button.config(text="매크로 시작", bg='lightgreen')
            if self.macro_thread:
                self.macro_thread.join(timeout=1)

    def quit_program(self):
        if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
            self.is_macro_running = False  # 매크로 중지
            if self.macro_thread:
                self.macro_thread.join(timeout=1.0)  # 스레드 종료 대기
            self.window.quit()

    def run_macro(self):
        while self.is_macro_running:
            try:
                pyautogui.press('space')
                
                # 클릭 10번
                for _ in range(10):
                    if not self.is_macro_running:
                        return
                    pyautogui.press('s')
                    time.sleep(0.1)
                
                if self.count < 3:
                    time.sleep(1)
                    pyautogui.press('space')
                    self.count += 1
                else:
                    time.sleep(15)
                    pyautogui.press('esc')
                    self.count = 0

            except Exception as e:
                # GUI 스레드에 안전하게 에러 메시지 표시
                self.window.after(0, lambda: messagebox.showerror("오류", f"매크로 실행 중 오류 발생: {str(e)}"))
                self.is_macro_running = False
                self.window.after(0, lambda: self.macro_button.config(text="매크로 시작", bg='lightgreen'))
                break

        # 다음 반복 예약
        self.window.after(100, self.run_macro)
        
    def run(self):
        self.window.mainloop()

        

# 프로그램 실행
if __name__ == "__main__":
    app = SimpleApp()
    app.run()
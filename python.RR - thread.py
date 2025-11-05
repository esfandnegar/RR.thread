import threading
import queue

# صف اشتراکی برای پردازه‌ها
ready_queue = queue.Queue()
lock = threading.Lock()

# زمان فعلی سیستم مشترک بین نخ‌ها
current_time = [0]

# تابع اجرای پردازه‌ها (توسط نخ‌ها)
def execute_processes(thread_name, burst_time, arrival_time, quantum, rem_bt, ct, wt, finished, total_processes):
    while True:
        with lock:
            if finished[0] >= total_processes:
                break

            if ready_queue.empty():
                # هیچ پردازه‌ای آماده نیست، زمان را جلو ببریم
                current_time[0] += 1
                continue

            i = ready_queue.get()
            # جلو بردن زمان اگر پردازه هنوز نرسیده
            if current_time[0] < arrival_time[i]:
                current_time[0] = arrival_time[i]

            exec_start = current_time[0]

        # اجرای پردازه
        exec_time = min(rem_bt[i], quantum)
        rem_bt[i] -= exec_time
        with lock:
            current_time[0] += exec_time
            if rem_bt[i] == 0:
                ct[i] = current_time[0]
                wt[i] = ct[i] - arrival_time[i] - burst_time[i]
                finished[0] += 1
            else:
                ready_queue.put(i)


def main():
    n = int(input("Enter number of processes: "))
    burst_time = []
    arrival_time = []
    processes = [i + 1 for i in range(n)]

    for i in range(n):
        at = int(input(f"Enter Arrival Time for Process P{i+1}: "))
        bt = int(input(f"Enter Burst Time for Process P{i+1}: "))
        arrival_time.append(at)
        burst_time.append(bt)

    quantum = int(input("Enter Time Quantum: "))

    rem_bt = burst_time.copy()
    ct = [0] * n
    wt = [0] * n
    finished = [0]  # لیست برای قابلیت اشتراک بین نخ‌ها

    # اضافه کردن پردازه‌ها به صف
    for i in range(n):
        ready_queue.put(i)

    # ایجاد دو نخ همزمان
    t1 = threading.Thread(target=execute_processes, args=("Thread-1", burst_time, arrival_time, quantum, rem_bt, ct, wt, finished, n))
    t2 = threading.Thread(target=execute_processes, args=("Thread-2", burst_time, arrival_time, quantum, rem_bt, ct, wt, finished, n))

    # اجرای نخ‌ها
    t1.start()
    t2.start()

    # انتظار برای پایان هر دو نخ
    t1.join()
    t2.join()

    # نمایش خروجی نهایی
    print("\n--- Final Round Robin (Dual Thread Shared Queue) ---")
    print(f"Time Quantum = {quantum}\n")
    print("P#\tA.T\tB.T\tEnd Time\tW.T")
    for i in range(n):
        print(f"P{i+1}\t{arrival_time[i]}\t{burst_time[i]}\t{ct[i]}\t\t{wt[i]}")

    avg_wt = sum(wt) / n
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")


if __name__ == "__main__":
    main()
import subprocess
res = subprocess.run([r'C:\Users\haris\OneDrive\Desktop\HCL\HclProject\ticket-ai\venv\Scripts\pytest.exe', 'test_nlp.py', '-v'], capture_output=True, text=True)
with open('err.txt', 'w', encoding='utf-8') as f:
    f.write(res.stdout)
    f.write("\nSTDERR:\n")
    f.write(res.stderr)

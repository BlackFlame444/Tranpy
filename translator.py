import os
import re
import logging
from tqdm import tqdm
from deep_translator import GoogleTranslator
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime

# Suppress HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Directories for logs and translated documents
log_directory = "/home/ish/tranpy/Logs"
translated_directory = "/home/ish/tranpy/Translated_Docs"
os.makedirs(log_directory, exist_ok=True)
os.makedirs(translated_directory, exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
success_logger = logging.getLogger("success")
error_logger = logging.getLogger("error")
handler_success = logging.FileHandler(f"{log_directory}/success.log")
handler_error = logging.FileHandler(f"{log_directory}/error.log")
success_logger.addHandler(handler_success)
error_logger.addHandler(handler_error)

def translate_text(text):
    translator = GoogleTranslator(source='auto', target='en')
    lines = text.split('\n')
    translated_lines = []
    progress = tqdm(lines, desc="Translating", unit="line")
    for line in progress:
        match = re.search(r'[\u4e00-\u9fff]+', line)
        if match:
            translated_part = translator.translate(match.group())
            translated_line = line.replace(match.group(), translated_part)
            translated_lines.append(translated_line)
        else:
            translated_lines.append(line)
    return '\n'.join(translated_lines)

def process_translation(input_text, output_path, counters):
    try:
        translated_text = translate_text(input_text)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
        success_logger.info(f"Translated successfully: {output_path}")
        counters['success'] += 1
        print("✶ Translation Successful ✶")
    except Exception as e:
        error_logger.error(f"Failed to translate: {str(e)}")
        counters['failed'] += 1
        print(f"Translation failed: {str(e)}")

def main():
    print("TRANPY ✶ translate what other bots can’t!\n v.0.1.1 [file translator written in python]\n")
    print("To start, please enter text, file path, or file URL you wish to translate: ")
    counters = {'success': 0, 'failed': 0}
    user_input = input()
    start_time = datetime.datetime.now()

    if os.path.exists(user_input):
        filename, file_ext = os.path.splitext(os.path.basename(user_input))
        output_path = f"{translated_directory}/{filename}_en{file_ext}"
        with open(user_input, 'r', encoding='utf-8') as file:
            input_text = file.read()
        process_translation(input_text, output_path, counters)
    elif user_input.startswith("http"):
        try:
            response = requests.get(user_input, verify=False)
            filename, file_ext = os.path.splitext(os.path.basename(user_input.split('?')[0]))
            output_path = f"{translated_directory}/{filename}_en{file_ext}"
            process_translation(response.text, output_path, counters)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {str(e)}")
    else:
        output_path = f"{translated_directory}/translated_text_en.txt"
        process_translation(user_input, output_path, counters)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print("———————————————————————————————————————————————")
    print(f"  {user_input}")
    print(f"Translating: 100%|| {counters['success']+counters['failed']}  {duration}, 2.50line/s]")
    print("———————————————————————————————————————————————")
    print("          ✶ Translation Successful ✶            ")
    print("———————————————————————————————————————————————")
    print("                  ✕ Report ✕                    ")
    print(f"    TIME:{end_time.strftime('%d-%m-%Y | %H:%M:%S')}               ")
    print(f"    LOCATION:{output_path}")
    print(f"    Successful  {counters['success']:02d}   |   {counters['failed']:02d}  Failed/Errors      ")
    print("———————————————————————————————————————————————")
    print("  ✕ Do you wish to translate another file?")
    print("  [Y] Yes  [N] Exit")
    print("———————————————————————————————————————————————")
    decision = input().strip().upper()
    if decision == 'Y':
        main()

if __name__ == "__main__":
    main()
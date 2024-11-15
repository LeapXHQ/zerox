from py_zerox.pyzerox import zerox
import asyncio
import json
async def main():
    file_path = "/Users/udaydhillon/Downloads/Checkbox-handwritten.pdf"
    zerox_result = await zerox(file_path=file_path, temp_dir= "./temp")
    markdown = ""
    for page in zerox_result.pages:
        markdown += page.content + "\n"

    print(markdown)
    result = {"markdown": markdown}
    # # print(result)
    # with open("sample_output.txt", "w") as f:
    #     f.write(json.dumps(result))
if __name__ == "__main__":
    asyncio.run(main())
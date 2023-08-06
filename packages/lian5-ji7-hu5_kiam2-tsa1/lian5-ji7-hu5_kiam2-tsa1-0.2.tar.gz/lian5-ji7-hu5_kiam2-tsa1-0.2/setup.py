from setuptools import setup, find_packages
setup(
  name = 'lian5-ji7-hu5_kiam2-tsa1',
  version = '0.2',
  packages = find_packages(exclude=["test*", "tests"]),
  install_requires=['tai5-uan5_gian5-gi2_kang1-ku7'],

  author = '意傳',
  author_email = 'a8568730@gmail.com',
  description = '臺羅連字符檢查',
  license="MIT",
  keywords = ['台灣閩南語', '書寫', '羅馬字', '檢查', '連字符'], 
  url = 'https://github.com/i3thuan5/lian5-ji7-hu5_kiam2-tsa1', 
  project_urls={
        "Bug Tracker": "https://github.com/i3thuan5/lian5-ji7-hu5_kiam2-tsa1/issues/",
        "Documentation": "https://github.com/i3thuan5/lian5-ji7-hu5_kiam2-tsa1",
        "Source Code": "https://github.com/i3thuan5/lian5-ji7-hu5_kiam2-tsa1",
    }
)
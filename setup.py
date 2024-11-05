from setuptools import setup, find_packages

with open('readme.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SuperQQBot',
    version='2024.11.6',  # 版本号应为标准格式，例如 '0.0.1'
    packages=find_packages(where='SuperQQBot'),  # 自动查找所有包
    package_dir={'': 'SuperQQBot'},  # 指定包的根目录
    url='https://gitee.com/SuperQQBot/SuperQQBot',
    license='GNU General Public License v2.0 (GPL2.0)',
    author='Supercmd',
    author_email='trustedinster@outlook.com',
    description='新一代QQ机器人SDK',
    long_description=long_description,  # 读取 README.md 文件作为长描述
    long_description_content_type='text/markdown',  # 指定长描述的格式为 Markdown
    classifiers=[
        'Development Status :: 3 - Alpha',  # 开发状态
        'Intended Audience :: Developers',  # 目标受众
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',  # 许可证
        'Programming Language :: Python :: 3',  # 支持的 Python 版本
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'asyncio~=3.4.3',
        'PyYAML~=6.0.2',
        'python-dateutil~=2.9.0.post0',
        'requests~=2.32.3',
        'requests~=2.32.3',
        'charset-normalizer<4,>=2',
        'idna<4,>=2.5',
        'urllib3<3,>=1.21.1',
        'certifi>=2017.4.17',
        'pytz~=2024.2',
        'datetime~=5.5',
        'bottle~=0.13.2'
    ],
    include_package_data=True,  # 包含包中的数据文件
    python_requires='>=3.8',  # 最低 Python 版本要求
)

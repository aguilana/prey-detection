from setuptools import setup, find_packages

setup(
    name="prey_detection",
    version="0.1.0",
    description="A computer vision system for detecting cats with prey",
    author="Nick Aguila",
    author_email="nick@nickaguila.me",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "prey-record=scripts.record_video:main",
            "prey-motion=scripts.motion_detect:main",
            "prey-extract=scripts.extract_frames:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

# Intelligent ATS - Enhance Your Resume for ATS

🎯 **Intelligent ATS** helps you enhance your resume by analyzing it against job descriptions using advanced AI techniques. It provides a match percentage, recommendations, and missing keywords to improve your resume and increase your chances of getting hired.

## Features

- Upload your resume and job description.
- Get a detailed analysis with a match percentage.
- Receive recommendations and identify missing keywords.
- Improve your resume to increase your chances of getting hired.
- Store evaluation results in MongoDB for future reference.

## Prerequisites

- Python 3.7+
- MongoDB Atlas account
- Google Cloud API key for Generative AI

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Addi2004/intelligent-ats.git
    cd intelligent-ats
    ```

2. Set up a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of your project and add the following environment variables:

    ```env
    GOOGLE_API_KEY=your_google_api_key
    MONGODB_URI=your_mongodb_uri
    ```

    Replace `your_google_api_key` with your actual Google Cloud API key and `your_mongodb_uri` with your MongoDB URI.

## Usage

1. Run the Streamlit app:

    ```sh
    streamlit run app1.py
    ```

2. Navigate to `http://localhost:8501` in your web browser.

3. Use the sidebar to navigate between the Home and ATS Evaluation pages.

4. On the ATS Evaluation page, paste the job description and upload your resume (PDF or DOCX format).

5. Click the **Submit** button to get your resume evaluated.

6. View the evaluation results, including the match percentage, missing keywords, candidate summary, and experience. The results are also saved to MongoDB.

## MongoDB Setup

1. Log in to your MongoDB Atlas account and create a new cluster.
2. Add your IP address to the Network Access whitelist.
3. Create a database user with the necessary permissions.
4. Copy the MongoDB URI and add it to your `.env` file as `MONGODB_URI`.

## Project Structure

- `app1.py`: Main Streamlit application file.
- `requirements.txt`: List of required Python packages.
- `.env`: Environment variables file (not included in the repository).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [PyMongo](https://pypi.org/project/pymongo/)
- [Google Generative AI](https://cloud.google.com/generative-ai)
- [docx2txt](https://pypi.org/project/docx2txt/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)

---

Feel free to customize this README file as needed. If you have any questions or encounter any issues, please open an issue on GitHub.

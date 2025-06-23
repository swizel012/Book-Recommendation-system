# 📚 Genre-Based Book Recommendation System

This is a Flask web application that recommends top-rated books based on the selected genre. It uses Goodreads data to provide recommendations, factoring in both average ratings and the number of user ratings for each book.
![Animation Preview](animation5.gif)  

## 🚀 Features

- Genre-based filtering using a clean dropdown UI
- Ranking algorithm that considers both **average rating** and **popularity**
- Simple and elegant interface styled with Tailwind CSS
- Displays top 10 books per genre

## 📁 Dataset

The app uses a cleaned version of Goodreads data in CSV format, including:

- `Book`
- `Author`
- `Genres` (list format)
- `Avg_Rating`
- `Num_Ratings`

📂 **Path**:  
`goodreads_data.csv`

## 🧠 Recommendation Logic

Books are ranked using a weighted score that balances:

- **R** = average rating for the book  
- **v** = number of ratings  
- **m** = 80th percentile of the number of ratings  
- **C** = mean rating across all books in the genre

The score is calculated using:
Score = (v / (v + m)) * R + (m / (v + m)) * C

This helps prioritize well-rated and widely-read books.

## 🛠️ How to Run

### 🔧 Prerequisites
Install the required packages:
pip install flask pandas
▶️ Run the app
python app.py
Visit http://127.0.0.1:5000 in your browser.

📸 UI Preview

📂 File Structure
├── app.py
├── goodreads_data.csv
├── templates/
│   ├── index.html
│   └── recommendations.html
├── animation5.gif (Application recording)
└── README.md

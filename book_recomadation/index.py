import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from tkinter import ttk, messagebox

df = pd.read_csv(r"D:\data science\book_recomadation\book_data.csv")

df = df.fillna('')

df['Features'] = (
    df['Author'] + " " +
    df['Original language'] + " " +
    df['Genre']
)


tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Features'])


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def recommend(title):
    if title not in df['Book'].values:
        return pd.DataFrame(columns=['Book', 'Author'])
    idx = df.index[df['Book'] == title][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:6]]
    return df.iloc[top_indices][['Book', 'Author', 'Genre']]

#GUI 
root = tk.Tk()
root.title("Book Recommendation System")
root.geometry("600x350")

tk.Label(root, text="Enter Book Title:", font=("Arial", 12)).pack(pady=5)
search_entry = tk.Entry(root, font=("Arial", 12), width=40)
search_entry.pack(pady=5)

columns = ["Book", "Author", "Genre"]
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.pack(expand=True, fill="both", pady=5)


def search_books():
    title = search_entry.get().strip()
    if not title:
        messagebox.showwarning("Input Error", "Please enter a book title.")
        return
    results = recommend(title)
    for row in tree.get_children():
        tree.delete(row)
    if results.empty:
        messagebox.showinfo("No Results", "No similar books found.")
    else:
        for _, row in results.iterrows():
            tree.insert("", tk.END, values=list(row))

tk.Button(root, text="Search", command=search_books, font=("Arial", 12)).pack(pady=5)

root.mainloop()

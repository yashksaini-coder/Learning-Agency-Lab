import os
import matplotlib.pyplot as plt
import seaborn as sns
import time

def create_plot_directory():
    """
    Function to create a folder named "plots" one folder above the current directory
    """
    # Get the current working directory
    current_dir = os.getcwd()
    # Navigate to the parent directory
    parent_dir = os.path.dirname(current_dir)
    
    # Create a directory named "plots" in the parent directory if it doesn't exist
    plots_dir = os.path.join(parent_dir, "plots")
    if not os.path.exists(plots_dir):
        os.mkdir(plots_dir)

feats = [
    "text_length","text_length_p","text_length_pc","text_length_ppr","text_length_pcpr",
    "word_count","word_count_p","word_count_pc","word_count_ppr","word_count_pcpr",
    "unique_word_count","unique_word_count_p","unique_word_count_pc","unique_word_count_ppr","unique_word_count_pcpr",
    "splling_err_num","splling_err_num_p","splling_err_num_pc","splling_err_num_ppr","splling_err_num_pcpr"
]

def Histogram_plot(train):
    os.makedirs("plots", exist_ok=True)
    sns.set(rc={'figure.figsize': (15, 15)})

    histogram_plot = train[feats + ["score"]].hist(bins=50)
    plt.savefig("plots/Histogram_plot.png")
    plt.show()
    time.sleep(2.0)
    plt.close()

def Boxplot(data, features, num_features_per_plot=5):
    num_plots = (len(features) + num_features_per_plot - 1) // num_features_per_plot  # Calculate the number of plots needed
    for i in range(num_plots):
        start_idx = i * num_features_per_plot
        end_idx = (i + 1) * num_features_per_plot
        plt.figure(figsize=(12, 2))
        sns.boxplot(data=data[features[start_idx:end_idx]], orient="h")
        plt.title(f'Boxplot {i+1}')
        plt.savefig(f"plots/Boxplot_{i}.png")
        plt.show()
        time.sleep(2.0)
        plt.close()
        
def Coorelation_plot(data):
    correlation_matrix = data[["score"]+feats].corr()
    plt.figure(figsize=(20, 20))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.2)
    plt.title('Correlation Matrix')
    plt.savefig("plots/Correlation_plot.png")
    plt.show()
    time.sleep(2.0)
    plt.close()
    
def Scatter_subplots(train_feats, feats):
    os.makedirs("plots", exist_ok=True)  
    for col_idx in range(0, len(feats), 5):
        fig, axes = plt.subplots(1, 5, figsize=(25, 6))
        for i in range(0, 5):
            if col_idx + i < len(feats):
                sns.scatterplot(ax=axes[i], data=train_feats, x=feats[col_idx + i], y='score', color='steelblue')
                axes[i].set_title(feats[col_idx + i])  
        plt.tight_layout()  
        plt.savefig(f"plots/Scatter_Sub-plot_{col_idx}.png")  # Save the entire figure
        plt.close(fig)
    plt.show()
    time.sleep(2.0)
    plt.close()

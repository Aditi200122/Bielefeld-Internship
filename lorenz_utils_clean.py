
import numpy as np
import matplotlib.pyplot as plt
import re

def extract_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        names = set(re.findall(r'\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ([^:]+):', text))
    return names

# def count_donor_messages(file_path, donor):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     pattern = re.compile(r'^\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - (.*?):')
#     count = 0
#     all_senders = set()

#     for line in lines:
#         match = pattern.match(line)
#         if match:
#             sender = match.group(1)
#             all_senders.add(sender)
#             if sender == donor:
#                 count += 1

    # all_senders.discard(donor)
    # contact = all_senders.pop() if all_senders else "Unknown"

    # return contact, count

def count_donor_msgs_words(file_path, donor_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    message_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - (.*?): (.*)')
    msg_count = 0
    word_count = 0
    all_senders = set()

    for line in lines:
        match = message_pattern.match(line)
        if match:
            sender, message = match.groups()
            all_senders.add(sender)
            if sender == donor_name:
                msg_count += 1
                word_count += len(message.split())

    # The contact is the other person
    all_senders.discard(donor_name)
    contact = all_senders.pop() if all_senders else "Unknown"

    return contact, msg_count, word_count


def calculate_gini(counts):
    values = sorted(counts.values())
    n = len(values)
    total = sum(values)
    weighted_sum = sum((i + 1) * val for i, val in enumerate(values))
    return (2 * weighted_sum) / (n * total) - (n + 1) / n

def get_lorenz_points(counts):
    values = np.array(sorted(counts.values()))
    cumulative_msgs = np.cumsum(values) / values.sum()
    cumulative_msgs = np.insert(cumulative_msgs, 0, 0)
    cumulative_contacts = np.linspace(0, 1, len(values) + 1)
    return cumulative_contacts, cumulative_msgs

def plot_lorenz_curve(counts, donor_name="Donor"):
    x, y = get_lorenz_points(counts)
    gini = calculate_gini(counts)

    plt.figure(figsize=(6, 5))
    plt.plot(x * 100, y * 100, label="Lorenz Curve", color="blue")
    plt.plot([0, 100], [0, 100], linestyle="--", color="gray", label="Perfect Equality")
    plt.fill_between(x * 100, x * 100, y * 100, color="lightblue", alpha=0.3)
    plt.title(f"{donor_name} - Lorenz Curve (Gini = {gini:.3f})")
    plt.xlabel("Cumulative % of Contacts")
    plt.ylabel("Cumulative % of Messages")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

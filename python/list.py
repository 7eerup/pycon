subscription_list = ["ChatGPT", "Gemini", "Perplexity"]
print("\n=== Subscription List ===")
print("구독 리스트:", subscription_list)

# index()
position = subscription_list.index("Gemini")
print(f"{position}번째 서비스: {subscription_list[position]}")

# append()
subscription_list.append("Claude")
print("Claude 구독 추가:", subscription_list)

# remove()
subscription_list.remove("Perplexity")
print("Perplexity 구독 제거:", subscription_list)

# sort()
subscription_list.sort()
print(subscription_list)

# reverse=True
subscription_list.sort(reverse=True)
print(subscription_list)

# len()
print(f"구독 서비스 개수: {len(subscription_list)}")


if "Claude" in subscription_list:
    print("Claude 구독 중입니다.")
else:
    print("Claude 구독 중이 아닙니다.")
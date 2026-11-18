import argparse
import hashlib
import itertools
import re
import string
import sys

# Educational tool. Only crack hashes you own or have permission to test
# (your own test accounts, CTF challenges, etc).

COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "qwerty", "abc123",
    "111111", "123123", "admin", "letmein", "welcome", "monkey",
    "password1", "iloveyou", "1234567", "dragon", "master", "football",
]


def check_strength(password):
    score = 0
    reasons = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        reasons.append("too short (less than 8 characters)")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        reasons.append("no lowercase letters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        reasons.append("no uppercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        reasons.append("no digits")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    else:
        reasons.append("no special characters")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        reasons = ["this is one of the most common passwords in the world"]

    if re.fullmatch(r"(.)\1*", password):
        score = 0
        reasons.append("repeated single character")

    levels = ["Very weak", "Weak", "Weak", "Medium", "Medium", "Strong", "Very strong"]
    level = levels[min(score, len(levels) - 1)]

    return level, score, reasons


def hash_text(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()


def crack_dictionary(target_hash, algo, wordlist_path):
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            if hash_text(word, algo) == target_hash.lower():
                return word
    return None


def crack_bruteforce(target_hash, algo, max_length, charset):
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            guess = "".join(combo)
            if hash_text(guess, algo) == target_hash.lower():
                return guess
    return None


def main():
    parser = argparse.ArgumentParser(description="Password strength checker and dictionary hash cracker")
    sub = parser.add_subparsers(dest="mode", required=True)

    p1 = sub.add_parser("check", help="check password strength")
    p1.add_argument("password")

    p2 = sub.add_parser("crack", help="crack a hash using a wordlist")
    p2.add_argument("hash")
    p2.add_argument("--algo", default="md5", choices=["md5", "sha1", "sha256"])
    p2.add_argument("--wordlist", required=True)

    p3 = sub.add_parser("bruteforce", help="crack a short hash by trying every combination (slow)")
    p3.add_argument("hash")
    p3.add_argument("--algo", default="md5", choices=["md5", "sha1", "sha256"])
    p3.add_argument("--max-length", type=int, default=4)
    p3.add_argument("--charset", default=string.ascii_lowercase + string.digits)

    args = parser.parse_args()

    if args.mode == "check":
        level, score, reasons = check_strength(args.password)
        print("Password:", args.password)
        print("Strength:", level, "(score " + str(score) + "/7)")
        if reasons:
            print("Issues:")
            for r in reasons:
                print("  -", r)

    elif args.mode == "crack":
        print("Trying wordlist:", args.wordlist)
        result = crack_dictionary(args.hash, args.algo, args.wordlist)
        if result:
            print("FOUND:", result)
        else:
            print("Not found in this wordlist.")

    elif args.mode == "bruteforce":
        print("Brute forcing up to length", args.max_length, "- this can take a while")
        result = crack_bruteforce(args.hash, args.algo, args.max_length, args.charset)
        if result:
            print("FOUND:", result)
        else:
            print("Not found in this search space.")


if __name__ == "__main__":
    main()

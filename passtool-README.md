# Password Strength Checker & Hash Cracker

A Python tool with three modes:

1. **check** - rates how strong a password is and explains why
2. **crack** - tries to crack a hash using a wordlist (dictionary attack)
3. **bruteforce** - tries every possible combination up to a given length (very slow, only for short hashes)

## Disclaimer

Only crack hashes you own or have explicit permission to test (your own test accounts, CTF challenges). Cracking someone else's password hash without permission is illegal.

## Requirements

- Python 3.8+
- No external libraries

## Usage

### Check password strength

```
python passtool.py check "MyP@ssw0rd123"
```

```
Password: MyP@ssw0rd123
Strength: Very strong (score 7/7)
```

### Crack a hash with a wordlist

```
python passtool.py crack 5f4dcc3b5aa765d61d8327deb882cf99 --algo md5 --wordlist rockyou.txt
```

```
Trying wordlist: rockyou.txt
FOUND: password
```

### Brute force a short hash

```
python passtool.py bruteforce 900150983cd24fb0d6963f7d28e17f72 --algo md5 --max-length 3
```

Supported algorithms: `md5`, `sha1`, `sha256`.

## How it works

**Strength check:** adds points for length (8+ and 12+ chars), lowercase, uppercase, digits, special characters. Drops to zero automatically if the password is one of the most common ones in the world or is just one character repeated (like `aaaaaa`) - length alone doesn't make those safe.

**Dictionary crack:** reads a wordlist line by line, hashes each word with the chosen algorithm, and compares it to the target hash. This is exactly what tools like John the Ripper or hashcat do, just much simpler and slower.

**Brute force:** tries every combination of characters up to a chosen length. Grows extremely fast - lowercase+digits up to length 4 is ~1.7 million combinations, length 6 is already ~2 billion. This is why long passwords matter so much more than complex short ones.

## Limitations

- No salting support - real password databases use salted hashes (a random value mixed in before hashing), which this tool does not handle
- Dictionary mode is single-threaded, so it's much slower than real tools (hashcat uses the GPU)
- No rule-based mutations (like `password` -> `P@ssw0rd!`), just raw wordlist entries

## Plans

- [ ] Support salted hashes (if salt is known)
- [ ] Multithreaded wordlist cracking
- [ ] Simple mutation rules (leetspeak, capitalization, append numbers)

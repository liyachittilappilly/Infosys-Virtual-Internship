from g2p_en import G2p


def generate_pronoun(sentence, filename="exp_pronoun.txt"):
    #sentence to words
    words = sentence.split()
    g2p = G2p()   # G2P model

    with open(filename, "w", encoding="utf-8") as f:
        f.write("Sentence:\n")
        f.write(sentence + "\n\n")
        f.write("Expected pronunciation (G2P):\n\n")

        for word in words:
            phonemes = g2p(word)                 # word to phonemes
            phonemes = [p for p in phonemes if p != " "]
            f.write(f"{word:<12} -> {' '.join(phonemes)}\n")

    print(f"Expected pronunciation saved to {filename}")


sentence = "She sells seashells by the seashore"
generate_pronoun(sentence)

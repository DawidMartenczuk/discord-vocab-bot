import discord
import nltk
import codecs

client = discord.Client()

vocab_file = 'vocab.txt'
vocab = []
operators = ['177815268825759744']
lastsave = 0


def vocab_open():
    global vocab
    f = open(vocab_file, 'r', encoding='utf8')
    vocab = f.readlines()
    vocab = [v.strip() for v in vocab]
    f.close()
    print("[vocab]: open " + str(len(vocab)) + " words")


def vocab_save():
    global vocab
    global lastsave
    f = open(vocab_file, 'w', encoding='utf8')
    for v in vocab:
        f.write(v + '\n')
    f.close()
    lastsave = len(vocab)
    print("[vocab]: save " + str(lastsave) + " words")


def vocab_write(w):
    global vocab
    if not w in vocab:
        vocab.append(w)
        l = len(vocab)
        print("[vocab]: " + str(l) + " words")
        if l > (lastsave + 100):
            vocab_save()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.dnd)
    vocab_open()


@client.event
async def on_message(message):
    if message.author.bot is\
            False or message.author.id == client.user.id:
        print((" > " if message.author.id == client.user.id else (" " + message.author.name + ("*" if message.author.id in operators else "") + ": ")) + message.content)
        if message.author.id != client.user.id:
            if message.author.id in operators:
                if message.content == 'vocab open':
                    vocab_open()
                    await client.send_message(message.channel, "Słownik został otwarty")
                    print("[vocab]: " + message.author.name + " opened vocab file")
                    return
                elif message.content == 'vocab view':
                    await client.send_message(message.channel, vocab)
                    print("[vocab]: " + message.author.name + " viewed vocab file")
                    return
                elif message.content == 'vocab save':
                    vocab_save()
                    await client.send_message(message.channel, "Słownik został zapisany")
                    print("[vocab]: " + message.author.name + " saved vocab file")
                    return
                elif message.content == 'vocab length':
                    print("[vocab]: " + str(len(vocab)))
                    await client.send_message(message.channel, "Słownik posiada " + str(500 + len(vocab)) + " słów")
                    return
            if message.content.find('http://') == -1 and message.content.find('https://') == -1:
                for w in nltk.word_tokenize(message.content):
                    vocab_write(w)

client.run('MzgyNTY3MDQ4NjQ5MjQ0Njcy.DYlBVA.9EhvFl3-BLW8tc-QzFv0U9ZsRMc')
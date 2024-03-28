import logging as log
import os
import app


def chatcompletion(client, system, chat_history):

    log.debug("chatcompletion:\n system: %s\n chat_history: %s", system,
              chat_history)

    messages = [
        {
            "role": "system",
            "content": system
        },
    ]

    log.debug("AGENDA: %s", messages)
    log.debug("chat_history: %s", chat_history)

    messages.extend(chat_history)

    output = client.chat.completions.create(model=os.environ.get(
        "OPENAI_MODEL", "gpt-4"),
                                            messages=messages,
                                            temperature=0,
                                            max_tokens=1024,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0)

    return output.choices[0].message.content


def chat_call(login, user_input):

    log.info("app.chat_history: %s", app.chat_history)

    chat_history = app.chat_history.get(login, [])
    client = app.openai_client

    log.info("chat_history: %s", chat_history)

    system = ""
    with open(os.environ.get("PROMT", "promt.txt"), encoding="utf-8") as f:
        system = f.read()

    log.debug("Create chat message")

    in_msg = {"role": "user", "content": user_input}
    chat_history.append(in_msg)
    output = chatcompletion(client, system, chat_history)
    chat_history.append({"role": "assistant", "content": output})

    app.chat_history[login] = chat_history

    return output

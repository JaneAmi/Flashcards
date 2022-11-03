import json, os, random, logging, io, argparse


class Cards:
    all_cards = []

    def __init__(self, term, defin, mist=0):
        self.term = term
        self.defin = defin
        self.mist = mist
        Cards.all_cards.append({'term': term, 'def': defin, 'mist': mist})


def create_cards_incl():
    term_list = [x['term'] for x in Cards.all_cards]
    def_list = [y['def'] for y in Cards.all_cards]
    u_term = log_input('The card:')
    while u_term in term_list:
        u_term = log_input(f'The card "{u_term}" already exists. Try again:\n')
    u_def = log_input('The definition of the card:')
    while u_def in def_list:
        u_def = log_input(f'The definition "{u_def}" already exists. Try again:')
    Cards(u_term, u_def)
    log_print(f'The pair ("{u_term}": "{u_def}") has been added.')


def check_cards_incl():
    u_range = log_input('How many times to ask?')
    def_list = [y['def'] for y in Cards.all_cards]
    for _ in range(int(u_range)):
        r_card = random.randint(0, len(Cards.all_cards) - 1)
        u_answ = log_input(f"Print the definition of \"{Cards.all_cards[r_card]['term']}\":")
        if u_answ == Cards.all_cards[r_card]['def']:
            log_print('Correct!')
        elif u_answ in def_list:
            for d in Cards.all_cards:
                if u_answ == d['def']:
                    log_print(f"Wrong. The right answer is \"{Cards.all_cards[r_card]['def']}\", but your definition is correct for \"{d['def']}\"")
                    Cards.all_cards[r_card]['mist'] = Cards.all_cards[r_card]['mist'] + 1
        else:
            log_print(f"Wrong. The right answer is \"{Cards.all_cards[r_card]['def']}\".")
            Cards.all_cards[r_card]['mist'] += 1


def remove_card_incl():
    u_input = log_input('Which card?')
    for i in range(len(Cards.all_cards)):
        if Cards.all_cards[i]['term'] == u_input:
            Cards.all_cards = Cards.all_cards[:i] + Cards.all_cards[i + 1:]
            log_print('The card has been removed.')
            break
    log_print(f"Can't remove \"{u_input}\": there is no such card.")


def reset_stats_incl():
    for i in range(len(Cards.all_cards)):
        Cards.all_cards[i]['mist'] = 0
    log_print('Card statistics have been reset.')


def hardest_card_incl():
    hard_c, max_mis = [], 0
    for i in range(len(Cards.all_cards)):
        if Cards.all_cards[i]['mist'] != 0 and (Cards.all_cards[i]['mist'] > max_mis or Cards.all_cards[i]['mist'] == max_mis):
            max_mis = Cards.all_cards[i]['mist']
            hard_c.append(Cards.all_cards[i]['term'])
    if max_mis == 0:
        log_print('There are no cards with errors.')
    elif len(hard_c) > 1:
        hc_list = [f'"{x}"' for x in hard_c]
        log_print(f'The hardest cards are {", ".join(hc_list)}. You have {max_mis} errors answering it.\n')
    else:
        log_print(f'The hardest card is "{hard_c[0]}". You have {max_mis} errors answering it.\n')


def import_cards_incl(cards_file):
    if os.access(cards_file, os.F_OK):
        with open(cards_file, 'r') as c_file:
            cards = ''.join(c_file.readlines())
        if cards:
            cards = list(json.loads(cards))
        else:
            cards = []
        log_print(f'{len(cards)} cards have been loaded.')
        term_list = [x['term'] for x in Cards.all_cards]
        if cards:
            for i in range(len(cards)):
                if cards[i]['term'] in term_list:
                    for y in range(len(Cards.all_cards)):
                        if cards[i]['term'] == Cards.all_cards[y]['term']:
                            Cards.all_cards[y]['def'] = cards[i]['def']
                else:
                    Cards.all_cards.append(cards[i])
        # for i in cards:
        #     cards_d[i] = cards[i]
    else:
        log_print('File not found.')


def export_cards(cards_file):
    with open(cards_file, 'w') as c_file:
        json.dump(Cards.all_cards, c_file)
    log_print(f'{len(Cards.all_cards)} cards have been saved.')


def log_print(p_string):
    print(p_string)
    logger.debug(p_string)


def log_input(p_string):
    print(p_string)
    logger.debug(p_string)
    u_input = input()
    logger.debug(u_input)
    return u_input


def log_file():
    u_input = log_input('File name:')
    with open(u_input, 'w') as file:
        print(stream.getvalue(), file=file)
    log_print('The log has been saved.')


def main_incl():
    u_action = log_input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
    if u_action == 'add':
        create_cards_incl()
    elif u_action == 'remove':
        remove_card_incl()
    elif u_action == 'import':
        u_cards_file = log_input('File name:')
        import_cards_incl(u_cards_file)
    elif u_action == 'export':
        u_cards_file = log_input('File name:')
        export_cards(u_cards_file)
    elif u_action == 'ask':
        check_cards_incl()
    elif u_action == 'log':
        log_file()
    elif u_action == 'hardest card':
        hardest_card_incl()
    elif u_action == 'reset stats':
        reset_stats_incl()
    elif u_action == 'exit':
        if args.export_to:
            export_cards(args.export_to)
        print('Bye bye!')
        Cards.all_cards = 'fin'


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')
    parser.add_argument('--export_to')
    args = parser.parse_args()
    if args.import_from:
        import_cards_incl(args.import_from)
    while Cards.all_cards != 'fin':
        main_incl()

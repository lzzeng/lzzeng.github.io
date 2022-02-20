import sys
import os
import argparse
import json
import datetime
import re
import subprocess
import pinyin
from copy import copy


class MyPass(object):
    def __init__(self, file_passwd='./passwd'):
        self.passwd_book = None
        self.file_passwd = file_passwd
        self.args = None
        # self.encrypt_head = 'MYPASSWD_HEAD'
        self.encrypt_head = bytes('MYPASSWD_HEAD', encoding="utf8")
        self.secret = ''

    def decrypt(self, content, encode=False, decode=True):
        """ bytes -> str
        """
        if len(self.secret) == 0:
            print("Warning: the secret is empty")
        elif decode and not content.startswith(self.encrypt_head):
            print("The content has already been decrypt")
            return content

        content = content[len(self.encrypt_head):]

        from itertools import cycle
        result = bytes()
        temp = cycle(self.secret)
        for ch in content:
            result += bytes(chr(ch ^ ord(next(temp))), encoding="utf8")

        return result.decode(encoding="utf8")

    def encrypt(self, content, encode=True, decode=False):
        """ bytes -> bytes
        """
        if len(self.secret) == 0:
            print("Warning: the secret is empty")
        elif encode and content.startswith(self.encrypt_head):
            print("The content has already been encrypt")
            return content

        from itertools import cycle
        # result = bytes(self.encrypt_head, encoding="utf8")
        result = self.encrypt_head
        temp = cycle(self.secret)

        # for ch in content:
        for bt in content:
            # result += bytes(chr(ord(ch) ^ ord(next(temp))), encoding="utf8")
            result += bytes(chr(bt ^ ord(next(temp))), encoding="utf8")

        # return result.decode()
        # return result.decode(encoding="utf8")
        return result

    def check_passwd_book(self):
        if self.passwd_book is None:
            try:
                with open(self.file_passwd, 'rb') as fp:
                    s = self.decrypt(fp.read())
                    self.passwd_book = json.loads(s)
            except FileNotFoundError:
                with open(self.file_passwd, 'wb') as fw:
                    fw.write(self.encrypt(bytes("{}", encoding="utf8")))
                    self.passwd_book = {}
            except Exception as e:
                try:
                    with open(self.file_passwd, 'r') as fp:
                        s = json.dumps(eval(fp.read()))
                        self.passwd_book = json.loads(s)
                except Exception:
                    print("check: Error\n")
                    sys.exit(1)

    def set_passwd(self, pk, psw):
        new_info = {
            "passwd": psw,
            "date": datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        }
        if self.passwd_book.get(pk):
            if self.passwd_book.get(pk)[0].get("passwd") == psw:
                print("Already exists:", self.passwd_book.get(pk)[0].get("date"), "******")
                return
        self.passwd_book.setdefault(pk, []).insert(0, new_info)
        print("New item: {}[{}]".format(pk, psw))

    def search_passwd(self, pks):
        if not pks:
            return

        pk = '.*'.join(pks)
        if 2 == len(pks):
            pk += '|' + '.*'.join(pks[::-1])

        pk2 = pk
        pk2s = ''.join(pks)
        if '+' not in pk2s and '*' not in pk2s and '?' not in pk2s:
            pk2 = '.*'.join(pk2s)
            if 2 == len(pks):
                pk2 += '|' + '.*'.join(''.join(pks[::-1]))

        k_mat = []
        if pk in self.passwd_book:
            k_mat.append(pk)  # strict match, limit 1
        else:
            try:
                pk_patt = re.compile(pk)
                pk2_patt = re.compile(pk2)  # match method 2
                # pk2_patt = pk_patt
                for k in self.passwd_book:
                    # if k == pk:
                    #     k_mat.append(k)  # strict match, limit 1
                    #     break
                    if pk == str(k).lower():
                        k_mat = [k]  # ignore case, limit 1
                        break
                    if pk_patt.search(str(k).lower()) or pk_patt.search(k):
                        k_mat.append(k)
                        continue
                    k2 = pinyin.get_initial(k, delimiter="")  # lowercase in default
                    if k2 == pk:
                        k_mat = [k]  # strict match initial letters, limit 1
                        break
                    # if pk_patt.search(str(k2).lower()) or pk_patt.search(k2):
                    if pk2_patt.search(str(k2).lower()) or pk2_patt.search(k2):
                        k_mat.append(k)
                        continue
                    k3 = pinyin.get(k, format="strip")
                    if pk_patt.search(str(k3).lower()) or pk_patt.search(k3):
                        k_mat.append(k)
                        continue
            except Exception:
                pass

        for mk in k_mat:
            print("{}:".format(mk))
            for it in self.passwd_book.get(mk):
                print('{}: {}\n'.format(it.get('date'), it.get('passwd')))

        # 000

    #        if pk in self.passwd_book:
    #            for it in self.passwd_book.get(pk):
    #                print('{}: {}'.format(it.get('date'), it.get('passwd')))
    #        else:
    #            try:
    #                pk_patt = re.compile(pk)
    #                for k in self.passwd_book:
    #                    if pk_patt.search(str(k).lower()) or pk_patt.search(k):
    #                        print("\n{}:".format(k))
    #                        for it in self.passwd_book.get(k):
    #                            print('{}: {}'.format(it.get('date'), it.get('passwd')))
    #                print()
    #            except Exception:
    #                print("Error")
    #                sys.exit(1)

    def get_passwd(self, pk, fmt_json=False):
        if pk in self.passwd_book:
            if fmt_json:
                # print({pk: self.passwd_book.get(pk)})
                print(json.dumps({pk: self.passwd_book.get(pk)}, indent=2))
            else:
                for it in self.passwd_book.get(pk):
                    print('{}: {}'.format(it.get('date'), it.get('passwd')))
                    break  # limit 1
        else:
            if pk == "keys" or pk == "all":
                # print("All keys:")
                print("-" * 48)
                for k in self.passwd_book.keys():
                    # print('<{}>'.format(k))
                    print('{}'.format(k), end=" | ")
                print()
                print("-" * 48)
                return
            elif pk == "info" or pk == "all-info":
                print("-" * 48)
                for k in self.passwd_book.keys():
                    # print('<{}>'.format(k))
                    print('{}'.format(k), end=" | ")
                print()
                print("-" * 48)
                # print(self.passwd_book)
                print(json.dumps(self.passwd_book))
                print("-" * 48)
                return
            print("Not exists:", pk)

    def add_multi_passwd(self, ex_file='./new_pass'):
        try:
            with open(ex_file, 'r') as fp:
                for line in fp.readlines():
                    pk, psw = line.split()
                    print("current line:", pk, psw)
                    self.set_passwd(pk, psw)
        except FileNotFoundError:
            print("No such file:", ex_file)
            sys.exit()
        except Exception:
            print("Error")
            sys.exit(1)

    def del_passwd(self, pk, rng=None):
        if pk in self.passwd_book:
            if not rng:
                del self.passwd_book[pk]
                print("Deleted:", pk)
                return True
            else:
                try:
                    a, b = 0, len(self.passwd_book[pk])
                    if ':' in rng:
                        a2, b2 = rng.split(":")
                    elif ',' in rng:
                        a2, b2 = rng.split(",")
                    else:
                        del self.passwd_book[pk][int(rng)]
                        print("Deleted: {}[{}]".format(pk, rng))
                        if not self.passwd_book[pk]:
                            del self.passwd_book[pk]
                            print("Deleted empty key:", pk)
                        return True

                    if a2 != "":
                        a = int(a2)

                    if b2 != "":
                        b = int(b2)

                    del self.passwd_book[pk][a:b]
                    print("Deleted range: {}[{}:{}]".format(pk, a2, b2))
                    if not self.passwd_book[pk]:
                        del self.passwd_book[pk]
                        print("Deleted empty key:", pk)

                    return True
                except Exception:
                    print("Error")
                    sys.exit(1)
        return False

    def update_file_passwd(self, ask=True, change_secret=False):
        is_update = False
        if change_secret:
            psw_1 = self.get_pass("New secret: ", twice=True)
            if psw_1 != self.secret:
                psw_2 = self.get_pass("Original secret: ", twice=False)
                if psw_2 != self.secret:
                    print("Wrong!")
                    sys.exit(1)
            self.secret = psw_1

        if ask:
            while True:
                yes_no = input("Update or not? [y/n/v]: ")
                if yes_no in ["y", "Y", "yes", "Yes", "YES"]:
                    is_update = True
                    break
                elif yes_no in ["v", "V"]:
                    print(json.dumps(self.passwd_book, indent=2))  # preview
                    continue
                else:
                    break

        if is_update:
            with open(self.file_passwd, 'wb') as fa:
                # fa.write(self.encrypt(json.dumps(self.passwd_book)))
                fa.write(self.encrypt(bytes(json.dumps(self.passwd_book), encoding="utf8")))
            print("Updated")
        else:
            print("Skipped update")

    def action_add(self):
        if not self.args.pk and not self.args.from_file:
            sys.exit()

        if not self.args.pk and self.args.rename:
            print("missing pk")
            sys.exit()

        self.get_secret()
        self.check_passwd_book()

        if self.args.from_file:
            print("trying add_multi_passwd ...\n")
            self.add_multi_passwd()

        if self.args.pk:
            if not self.args.rename:
                print("trying add_passwd for {} ...".format(self.args.pk))
                psw = self.get_pass("Password: ", twice=False)
                self.set_passwd(self.args.pk, psw)
            elif self.args.pk in self.passwd_book and self.args.rename != self.args.pk:
                try:
                    # rename: add new and del old
                    print("trying rename {} as {} ...".format(self.args.pk, self.args.rename))
                    src_item = self.passwd_book.get(self.args.pk)
                    if self.args.rename in self.passwd_book:
                        # merge when exists
                        src_item.extend(self.passwd_book.get(self.args.rename))
                        self.passwd_book[self.args.rename] = copy(src_item)  # no need to deepcopy
                        del self.passwd_book[self.args.pk]
                        print("merged")
                    else:
                        self.passwd_book[self.args.rename] = src_item
                        del self.passwd_book[self.args.pk]
                except Exception:
                    pass
            else:
                print("Skipped")
                sys.exit()

        self.update_file_passwd(change_secret=self.args.change_secret)

    def action_del(self):
        self.get_secret()
        self.check_passwd_book()
        if self.del_passwd(self.args.pk, rng=self.args.rng):
            self.update_file_passwd()

    def action_get(self):
        # self.secret = self.get_pass("Please input the secret: ")
        self.get_secret()
        self.check_passwd_book()
        self.get_passwd(self.args.pk, self.args.fmt_json)

    def action_search(self):
        self.get_secret()
        self.check_passwd_book()
        # self.search_passwd(self.args.pk)
        self.search_passwd(self.args.pks)

    def get_secret(self):
        # print("get sec ...")
        self.secret = os.getenv('mypass_secret')
        if self.secret is None:
            self.secret = self.get_pass("Please input the secret: ")

    @staticmethod
    def get_pass(msg, twice=False):
        sys.stdout.write(msg)
        sys.stdout.flush()
        subprocess.check_call(["stty", "-echo"])
        inp = input()

        if twice:
            sys.stdout.write("\nConfirm: ")
            sys.stdout.flush()
            subprocess.check_call(["stty", "-echo"])
            password2 = input()

            if inp == password2:
                print("\nOK")
            else:
                print("\nNot the same")
                subprocess.check_call(["stty", "echo"])
                sys.exit()

        subprocess.check_call(["stty", "echo"])
        print()
        return inp

    def main(self):
        parser = argparse.ArgumentParser(prog='PROG')
        subparsers = parser.add_subparsers(help='sub-command help')

        parser_a = subparsers.add_parser('add', help='add a specific key or add keys from file ./new_pass')
        parser_a.add_argument('pk', type=str, nargs='?', help='key name')
        parser_a.add_argument("-F", "--from-file", action="store_true", help="add keys from file ./new_pass")
        parser_a.add_argument("-S", "--change-secret", action="store_true", help="ask new secret for changing secret")
        parser_a.add_argument("-R", '--rename', type=str, help='rename')

        parser_b = subparsers.add_parser('del', help='del a specific key or del keys by range')
        parser_b.add_argument('pk', type=str, help='key name')
        parser_b.add_argument('-n', '--rng', type=str, help='range, e.g. 2:3 or 3: or 2,3')

        parser_c = subparsers.add_parser('get', help='get a specific key')
        parser_c.add_argument('pk', type=str, help='key name')
        parser_c.add_argument("-J", "--fmt-json", action="store_true", help="show in json format")

        parser_d = subparsers.add_parser('search', help='search keys')
        parser_d.add_argument('pks', type=str, nargs='+', help='key name pattern list')

        parser_a.set_defaults(func=self.action_add)
        parser_b.set_defaults(func=self.action_del)
        parser_c.set_defaults(func=self.action_get)
        parser_d.set_defaults(func=self.action_search)

        args = parser.parse_args()
        if not hasattr(args, 'func'):
            args = parser.parse_args(['-h'])

        self.args = args
        self.args.func()


if __name__ == '__main__':
    MyPass().main()

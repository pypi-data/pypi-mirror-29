"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
import os
import struct


class ChangePhoneRequest(TLObject):
    CONSTRUCTOR_ID = 0x70c32edb
    SUBCLASS_OF_ID = 0x2da17977

    def __init__(self, phone_number, phone_code_hash, phone_code):
        """
        :param str phone_number:
        :param str phone_code_hash:
        :param str phone_code:

        :returns User: Instance of either UserEmpty, User.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code

    def to_dict(self):
        return {
            '_': 'ChangePhoneRequest',
            'phone_number': self.phone_number,
            'phone_code_hash': self.phone_code_hash,
            'phone_code': self.phone_code
        }

    def __bytes__(self):
        return b''.join((
            b'\xdb.\xc3p',
            TLObject.serialize_bytes(self.phone_number),
            TLObject.serialize_bytes(self.phone_code_hash),
            TLObject.serialize_bytes(self.phone_code),
        ))

    @staticmethod
    def from_reader(reader):
        _phone_number = reader.tgread_string()
        _phone_code_hash = reader.tgread_string()
        _phone_code = reader.tgread_string()
        return ChangePhoneRequest(phone_number=_phone_number, phone_code_hash=_phone_code_hash, phone_code=_phone_code)


class CheckUsernameRequest(TLObject):
    CONSTRUCTOR_ID = 0x2714d86c
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, username):
        """
        :param str username:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.username = username

    def to_dict(self):
        return {
            '_': 'CheckUsernameRequest',
            'username': self.username
        }

    def __bytes__(self):
        return b''.join((
            b"l\xd8\x14'",
            TLObject.serialize_bytes(self.username),
        ))

    @staticmethod
    def from_reader(reader):
        _username = reader.tgread_string()
        return CheckUsernameRequest(username=_username)


class ConfirmPhoneRequest(TLObject):
    CONSTRUCTOR_ID = 0x5f2178c3
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, phone_code_hash, phone_code):
        """
        :param str phone_code_hash:
        :param str phone_code:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code

    def to_dict(self):
        return {
            '_': 'ConfirmPhoneRequest',
            'phone_code_hash': self.phone_code_hash,
            'phone_code': self.phone_code
        }

    def __bytes__(self):
        return b''.join((
            b'\xc3x!_',
            TLObject.serialize_bytes(self.phone_code_hash),
            TLObject.serialize_bytes(self.phone_code),
        ))

    @staticmethod
    def from_reader(reader):
        _phone_code_hash = reader.tgread_string()
        _phone_code = reader.tgread_string()
        return ConfirmPhoneRequest(phone_code_hash=_phone_code_hash, phone_code=_phone_code)


class DeleteAccountRequest(TLObject):
    CONSTRUCTOR_ID = 0x418d4e0b
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, reason):
        """
        :param str reason:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.reason = reason

    def to_dict(self):
        return {
            '_': 'DeleteAccountRequest',
            'reason': self.reason
        }

    def __bytes__(self):
        return b''.join((
            b'\x0bN\x8dA',
            TLObject.serialize_bytes(self.reason),
        ))

    @staticmethod
    def from_reader(reader):
        _reason = reader.tgread_string()
        return DeleteAccountRequest(reason=_reason)


class GetAccountTTLRequest(TLObject):
    CONSTRUCTOR_ID = 0x8fc711d
    SUBCLASS_OF_ID = 0xbaa39d88

    def __init__(self):
        super().__init__()
        self.result = None
        self.content_related = True

    def to_dict(self):
        return {
            '_': 'GetAccountTTLRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\x1dq\xfc\x08',
        ))

    @staticmethod
    def from_reader(reader):
        return GetAccountTTLRequest()


class GetAuthorizationsRequest(TLObject):
    CONSTRUCTOR_ID = 0xe320c158
    SUBCLASS_OF_ID = 0xbf5e0ff

    def __init__(self):
        super().__init__()
        self.result = None
        self.content_related = True

    def to_dict(self):
        return {
            '_': 'GetAuthorizationsRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'X\xc1 \xe3',
        ))

    @staticmethod
    def from_reader(reader):
        return GetAuthorizationsRequest()


class GetNotifySettingsRequest(TLObject):
    CONSTRUCTOR_ID = 0x12b3ad31
    SUBCLASS_OF_ID = 0xcf20c074

    def __init__(self, peer):
        """
        :param InputNotifyPeer peer:

        :returns PeerNotifySettings: Instance of either PeerNotifySettingsEmpty, PeerNotifySettings.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.peer = peer

    def to_dict(self):
        return {
            '_': 'GetNotifySettingsRequest',
            'peer': None if self.peer is None else self.peer.to_dict()
        }

    def __bytes__(self):
        return b''.join((
            b'1\xad\xb3\x12',
            bytes(self.peer),
        ))

    @staticmethod
    def from_reader(reader):
        _peer = reader.tgread_object()
        return GetNotifySettingsRequest(peer=_peer)


class GetPasswordRequest(TLObject):
    CONSTRUCTOR_ID = 0x548a30f5
    SUBCLASS_OF_ID = 0x53a211a3

    def __init__(self):
        super().__init__()
        self.result = None
        self.content_related = True

    def to_dict(self):
        return {
            '_': 'GetPasswordRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\xf50\x8aT',
        ))

    @staticmethod
    def from_reader(reader):
        return GetPasswordRequest()


class GetPasswordSettingsRequest(TLObject):
    CONSTRUCTOR_ID = 0xbc8d11bb
    SUBCLASS_OF_ID = 0xd23fb078

    def __init__(self, current_password_hash):
        """
        :param bytes current_password_hash:

        :returns account.PasswordSettings: Instance of PasswordSettings.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.current_password_hash = current_password_hash

    def to_dict(self):
        return {
            '_': 'GetPasswordSettingsRequest',
            'current_password_hash': self.current_password_hash
        }

    def __bytes__(self):
        return b''.join((
            b'\xbb\x11\x8d\xbc',
            TLObject.serialize_bytes(self.current_password_hash),
        ))

    @staticmethod
    def from_reader(reader):
        _current_password_hash = reader.tgread_bytes()
        return GetPasswordSettingsRequest(current_password_hash=_current_password_hash)


class GetPrivacyRequest(TLObject):
    CONSTRUCTOR_ID = 0xdadbc950
    SUBCLASS_OF_ID = 0xb55aba82

    def __init__(self, key):
        """
        :param InputPrivacyKey key:

        :returns account.PrivacyRules: Instance of PrivacyRules.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.key = key

    def to_dict(self):
        return {
            '_': 'GetPrivacyRequest',
            'key': None if self.key is None else self.key.to_dict()
        }

    def __bytes__(self):
        return b''.join((
            b'P\xc9\xdb\xda',
            bytes(self.key),
        ))

    @staticmethod
    def from_reader(reader):
        _key = reader.tgread_object()
        return GetPrivacyRequest(key=_key)


class GetTmpPasswordRequest(TLObject):
    CONSTRUCTOR_ID = 0x4a82327e
    SUBCLASS_OF_ID = 0xb064992d

    def __init__(self, password_hash, period):
        """
        :param bytes password_hash:
        :param int period:

        :returns account.TmpPassword: Instance of TmpPassword.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.password_hash = password_hash
        self.period = period

    def to_dict(self):
        return {
            '_': 'GetTmpPasswordRequest',
            'password_hash': self.password_hash,
            'period': self.period
        }

    def __bytes__(self):
        return b''.join((
            b'~2\x82J',
            TLObject.serialize_bytes(self.password_hash),
            struct.pack('<i', self.period),
        ))

    @staticmethod
    def from_reader(reader):
        _password_hash = reader.tgread_bytes()
        _period = reader.read_int()
        return GetTmpPasswordRequest(password_hash=_password_hash, period=_period)


class GetWallPapersRequest(TLObject):
    CONSTRUCTOR_ID = 0xc04cfac2
    SUBCLASS_OF_ID = 0x8ec35283

    def __init__(self):
        super().__init__()
        self.result = None
        self.content_related = True

    def to_dict(self):
        return {
            '_': 'GetWallPapersRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\xc2\xfaL\xc0',
        ))

    @staticmethod
    def from_reader(reader):
        return GetWallPapersRequest()


class RegisterDeviceRequest(TLObject):
    CONSTRUCTOR_ID = 0xf75874d1
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, token_type, token, other_uids):
        """
        :param int token_type:
        :param str token:
        :param list[int] other_uids:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.token_type = token_type
        self.token = token
        self.other_uids = other_uids

    def to_dict(self):
        return {
            '_': 'RegisterDeviceRequest',
            'token_type': self.token_type,
            'token': self.token,
            'other_uids': [] if self.other_uids is None else self.other_uids[:]
        }

    def __bytes__(self):
        return b''.join((
            b'\xd1tX\xf7',
            struct.pack('<i', self.token_type),
            TLObject.serialize_bytes(self.token),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.other_uids)),b''.join(struct.pack('<i', x) for x in self.other_uids),
        ))

    @staticmethod
    def from_reader(reader):
        _token_type = reader.read_int()
        _token = reader.tgread_string()
        reader.read_int()
        _other_uids = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _other_uids.append(_x)

        return RegisterDeviceRequest(token_type=_token_type, token=_token, other_uids=_other_uids)


class ReportPeerRequest(TLObject):
    CONSTRUCTOR_ID = 0xae189d5f
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, peer, reason):
        """
        :param InputPeer peer:
        :param ReportReason reason:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.peer = peer
        self.reason = reason

    def resolve(self, client, utils):
        self.peer = utils.get_input_peer(client.get_input_entity(self.peer))

    def to_dict(self):
        return {
            '_': 'ReportPeerRequest',
            'peer': None if self.peer is None else self.peer.to_dict(),
            'reason': None if self.reason is None else self.reason.to_dict()
        }

    def __bytes__(self):
        return b''.join((
            b'_\x9d\x18\xae',
            bytes(self.peer),
            bytes(self.reason),
        ))

    @staticmethod
    def from_reader(reader):
        _peer = reader.tgread_object()
        _reason = reader.tgread_object()
        return ReportPeerRequest(peer=_peer, reason=_reason)


class ResetAuthorizationRequest(TLObject):
    CONSTRUCTOR_ID = 0xdf77f3bc
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, hash):
        """
        :param int hash:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.hash = hash

    def to_dict(self):
        return {
            '_': 'ResetAuthorizationRequest',
            'hash': self.hash
        }

    def __bytes__(self):
        return b''.join((
            b'\xbc\xf3w\xdf',
            struct.pack('<q', self.hash),
        ))

    @staticmethod
    def from_reader(reader):
        _hash = reader.read_long()
        return ResetAuthorizationRequest(hash=_hash)


class ResetNotifySettingsRequest(TLObject):
    CONSTRUCTOR_ID = 0xdb7e1747
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self):
        super().__init__()
        self.result = None
        self.content_related = True

    def to_dict(self):
        return {
            '_': 'ResetNotifySettingsRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'G\x17~\xdb',
        ))

    @staticmethod
    def from_reader(reader):
        return ResetNotifySettingsRequest()


class SendChangePhoneCodeRequest(TLObject):
    CONSTRUCTOR_ID = 0x8e57deb
    SUBCLASS_OF_ID = 0x6ce87081

    def __init__(self, phone_number, allow_flashcall=None, current_number=None):
        """
        :param bool | None allow_flashcall:
        :param str phone_number:
        :param Bool | None current_number:

        :returns auth.SentCode: Instance of SentCode.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.allow_flashcall = allow_flashcall
        self.phone_number = phone_number
        self.current_number = current_number

    def to_dict(self):
        return {
            '_': 'SendChangePhoneCodeRequest',
            'allow_flashcall': self.allow_flashcall,
            'phone_number': self.phone_number,
            'current_number': self.current_number
        }

    def __bytes__(self):
        assert ((self.allow_flashcall or self.allow_flashcall is not None) and (self.current_number or self.current_number is not None)) or ((self.allow_flashcall is None or self.allow_flashcall is False) and (self.current_number is None or self.current_number is False)), 'allow_flashcall, current_number parameters must all be False-y (like None) or all me True-y'
        return b''.join((
            b'\xeb}\xe5\x08',
            struct.pack('<I', (0 if self.allow_flashcall is None or self.allow_flashcall is False else 1) | (0 if self.current_number is None or self.current_number is False else 1)),
            TLObject.serialize_bytes(self.phone_number),
            b'' if self.current_number is None or self.current_number is False else (b'\xb5ur\x99' if self.current_number else b'7\x97y\xbc'),
        ))

    @staticmethod
    def from_reader(reader):
        flags = reader.read_int()

        _allow_flashcall = bool(flags & 1)
        _phone_number = reader.tgread_string()
        if flags & 1:
            _current_number = reader.tgread_bool()
        else:
            _current_number = None
        return SendChangePhoneCodeRequest(phone_number=_phone_number, allow_flashcall=_allow_flashcall, current_number=_current_number)


class SendConfirmPhoneCodeRequest(TLObject):
    CONSTRUCTOR_ID = 0x1516d7bd
    SUBCLASS_OF_ID = 0x6ce87081

    def __init__(self, hash, allow_flashcall=None, current_number=None):
        """
        :param bool | None allow_flashcall:
        :param str hash:
        :param Bool | None current_number:

        :returns auth.SentCode: Instance of SentCode.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.allow_flashcall = allow_flashcall
        self.hash = hash
        self.current_number = current_number

    def to_dict(self):
        return {
            '_': 'SendConfirmPhoneCodeRequest',
            'allow_flashcall': self.allow_flashcall,
            'hash': self.hash,
            'current_number': self.current_number
        }

    def __bytes__(self):
        assert ((self.allow_flashcall or self.allow_flashcall is not None) and (self.current_number or self.current_number is not None)) or ((self.allow_flashcall is None or self.allow_flashcall is False) and (self.current_number is None or self.current_number is False)), 'allow_flashcall, current_number parameters must all be False-y (like None) or all me True-y'
        return b''.join((
            b'\xbd\xd7\x16\x15',
            struct.pack('<I', (0 if self.allow_flashcall is None or self.allow_flashcall is False else 1) | (0 if self.current_number is None or self.current_number is False else 1)),
            TLObject.serialize_bytes(self.hash),
            b'' if self.current_number is None or self.current_number is False else (b'\xb5ur\x99' if self.current_number else b'7\x97y\xbc'),
        ))

    @staticmethod
    def from_reader(reader):
        flags = reader.read_int()

        _allow_flashcall = bool(flags & 1)
        _hash = reader.tgread_string()
        if flags & 1:
            _current_number = reader.tgread_bool()
        else:
            _current_number = None
        return SendConfirmPhoneCodeRequest(hash=_hash, allow_flashcall=_allow_flashcall, current_number=_current_number)


class SetAccountTTLRequest(TLObject):
    CONSTRUCTOR_ID = 0x2442485e
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, ttl):
        """
        :param AccountDaysTTL ttl:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.ttl = ttl

    def to_dict(self):
        return {
            '_': 'SetAccountTTLRequest',
            'ttl': None if self.ttl is None else self.ttl.to_dict()
        }

    def __bytes__(self):
        return b''.join((
            b'^HB$',
            bytes(self.ttl),
        ))

    @staticmethod
    def from_reader(reader):
        _ttl = reader.tgread_object()
        return SetAccountTTLRequest(ttl=_ttl)


class SetPrivacyRequest(TLObject):
    CONSTRUCTOR_ID = 0xc9f81ce8
    SUBCLASS_OF_ID = 0xb55aba82

    def __init__(self, key, rules):
        """
        :param InputPrivacyKey key:
        :param list[InputPrivacyRule] rules:

        :returns account.PrivacyRules: Instance of PrivacyRules.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.key = key
        self.rules = rules

    def to_dict(self):
        return {
            '_': 'SetPrivacyRequest',
            'key': None if self.key is None else self.key.to_dict(),
            'rules': [] if self.rules is None else [None if x is None else x.to_dict() for x in self.rules]
        }

    def __bytes__(self):
        return b''.join((
            b'\xe8\x1c\xf8\xc9',
            bytes(self.key),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.rules)),b''.join(bytes(x) for x in self.rules),
        ))

    @staticmethod
    def from_reader(reader):
        _key = reader.tgread_object()
        reader.read_int()
        _rules = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _rules.append(_x)

        return SetPrivacyRequest(key=_key, rules=_rules)


class UnregisterDeviceRequest(TLObject):
    CONSTRUCTOR_ID = 0x3076c4bf
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, token_type, token, other_uids):
        """
        :param int token_type:
        :param str token:
        :param list[int] other_uids:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.token_type = token_type
        self.token = token
        self.other_uids = other_uids

    def to_dict(self):
        return {
            '_': 'UnregisterDeviceRequest',
            'token_type': self.token_type,
            'token': self.token,
            'other_uids': [] if self.other_uids is None else self.other_uids[:]
        }

    def __bytes__(self):
        return b''.join((
            b'\xbf\xc4v0',
            struct.pack('<i', self.token_type),
            TLObject.serialize_bytes(self.token),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.other_uids)),b''.join(struct.pack('<i', x) for x in self.other_uids),
        ))

    @staticmethod
    def from_reader(reader):
        _token_type = reader.read_int()
        _token = reader.tgread_string()
        reader.read_int()
        _other_uids = []
        for _ in range(reader.read_int()):
            _x = reader.read_int()
            _other_uids.append(_x)

        return UnregisterDeviceRequest(token_type=_token_type, token=_token, other_uids=_other_uids)


class UpdateDeviceLockedRequest(TLObject):
    CONSTRUCTOR_ID = 0x38df3532
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, period):
        """
        :param int period:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.period = period

    def to_dict(self):
        return {
            '_': 'UpdateDeviceLockedRequest',
            'period': self.period
        }

    def __bytes__(self):
        return b''.join((
            b'25\xdf8',
            struct.pack('<i', self.period),
        ))

    @staticmethod
    def from_reader(reader):
        _period = reader.read_int()
        return UpdateDeviceLockedRequest(period=_period)


class UpdateNotifySettingsRequest(TLObject):
    CONSTRUCTOR_ID = 0x84be5b93
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, peer, settings):
        """
        :param InputNotifyPeer peer:
        :param InputPeerNotifySettings settings:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.peer = peer
        self.settings = settings

    def to_dict(self):
        return {
            '_': 'UpdateNotifySettingsRequest',
            'peer': None if self.peer is None else self.peer.to_dict(),
            'settings': None if self.settings is None else self.settings.to_dict()
        }

    def __bytes__(self):
        return b''.join((
            b'\x93[\xbe\x84',
            bytes(self.peer),
            bytes(self.settings),
        ))

    @staticmethod
    def from_reader(reader):
        _peer = reader.tgread_object()
        _settings = reader.tgread_object()
        return UpdateNotifySettingsRequest(peer=_peer, settings=_settings)


class UpdatePasswordSettingsRequest(TLObject):
    CONSTRUCTOR_ID = 0xfa7c4b86
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, current_password_hash, new_settings):
        """
        :param bytes current_password_hash:
        :param account.PasswordInputSettings new_settings:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.current_password_hash = current_password_hash
        self.new_settings = new_settings

    def to_dict(self):
        return {
            '_': 'UpdatePasswordSettingsRequest',
            'current_password_hash': self.current_password_hash,
            'new_settings': None if self.new_settings is None else self.new_settings.to_dict()
        }

    def __bytes__(self):
        return b''.join((
            b'\x86K|\xfa',
            TLObject.serialize_bytes(self.current_password_hash),
            bytes(self.new_settings),
        ))

    @staticmethod
    def from_reader(reader):
        _current_password_hash = reader.tgread_bytes()
        _new_settings = reader.tgread_object()
        return UpdatePasswordSettingsRequest(current_password_hash=_current_password_hash, new_settings=_new_settings)


class UpdateProfileRequest(TLObject):
    CONSTRUCTOR_ID = 0x78515775
    SUBCLASS_OF_ID = 0x2da17977

    def __init__(self, first_name=None, last_name=None, about=None):
        """
        :param str | None first_name:
        :param str | None last_name:
        :param str | None about:

        :returns User: Instance of either UserEmpty, User.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.first_name = first_name
        self.last_name = last_name
        self.about = about

    def to_dict(self):
        return {
            '_': 'UpdateProfileRequest',
            'first_name': self.first_name,
            'last_name': self.last_name,
            'about': self.about
        }

    def __bytes__(self):
        return b''.join((
            b'uWQx',
            struct.pack('<I', (0 if self.first_name is None or self.first_name is False else 1) | (0 if self.last_name is None or self.last_name is False else 2) | (0 if self.about is None or self.about is False else 4)),
            b'' if self.first_name is None or self.first_name is False else (TLObject.serialize_bytes(self.first_name)),
            b'' if self.last_name is None or self.last_name is False else (TLObject.serialize_bytes(self.last_name)),
            b'' if self.about is None or self.about is False else (TLObject.serialize_bytes(self.about)),
        ))

    @staticmethod
    def from_reader(reader):
        flags = reader.read_int()

        if flags & 1:
            _first_name = reader.tgread_string()
        else:
            _first_name = None
        if flags & 2:
            _last_name = reader.tgread_string()
        else:
            _last_name = None
        if flags & 4:
            _about = reader.tgread_string()
        else:
            _about = None
        return UpdateProfileRequest(first_name=_first_name, last_name=_last_name, about=_about)


class UpdateStatusRequest(TLObject):
    CONSTRUCTOR_ID = 0x6628562c
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, offline):
        """
        :param Bool offline:

        :returns Bool: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.offline = offline

    def to_dict(self):
        return {
            '_': 'UpdateStatusRequest',
            'offline': self.offline
        }

    def __bytes__(self):
        return b''.join((
            b',V(f',
            b'\xb5ur\x99' if self.offline else b'7\x97y\xbc',
        ))

    @staticmethod
    def from_reader(reader):
        _offline = reader.tgread_bool()
        return UpdateStatusRequest(offline=_offline)


class UpdateUsernameRequest(TLObject):
    CONSTRUCTOR_ID = 0x3e0bdd7c
    SUBCLASS_OF_ID = 0x2da17977

    def __init__(self, username):
        """
        :param str username:

        :returns User: Instance of either UserEmpty, User.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.username = username

    def to_dict(self):
        return {
            '_': 'UpdateUsernameRequest',
            'username': self.username
        }

    def __bytes__(self):
        return b''.join((
            b'|\xdd\x0b>',
            TLObject.serialize_bytes(self.username),
        ))

    @staticmethod
    def from_reader(reader):
        _username = reader.tgread_string()
        return UpdateUsernameRequest(username=_username)

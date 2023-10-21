from lib.ydb.literals import Operator

types = {
    int: 'Int32',
    float: 'Double',
    bytes: 'String',
    bool: 'Bool'
}


class YdbQuery:
    def __init__(self) -> None:
        self.table: str
        self.database: str
        self._datamode = {
            'dec': self._getDeclare,
            'var': self._getVar
        }

    def generate_upsert(self, payload: dict) -> str:
        query = f"\rUPSERT INTO {self.table} ({','.join(i[1:] for i in payload.keys())}) VALUES ({','.join(i for i in payload.keys())});"
        return self._getHeader(payload) + query

    def generate_insert(self, payload: dict) -> str:
        query = f"\rINSERT INTO {self.table} ({','.join(i[1:] for i in payload.keys())}) VALUES ({','.join(i for i in payload.keys())});"
        return self._getHeader(payload) + query

    def generate_select(self, payload: dict | None, operation: Operator | None) -> str:
        query = f'\rSELECT * FROM {self.table}'
        if payload:
            query += f" WHERE {f' {operation} '.join(self._getWhere(key) for key in payload.keys())}"
            query = self._getHeader(payload) + query
        return query + ';'

    def generate_update(self, conditions: dict, payload: dict) -> str:
        query = f"\rUPDATE {self.table} SET {','.join(self._getWhere(key) for key in payload.keys())} WHERE {' AND '.join(self._getWhere(key) for key in conditions.keys())};"
        return self._getHeader(conditions | payload) + query

    def generate_delete(self, payload: dict) -> str:
        query = f"\rDELETE FROM {self.table} WHERE {' AND '.join(self._getWhere(key) for key in payload.keys())};"
        return self._getHeader(payload) + query

    def _getHeader(self, payload: dict) -> str:
        header = f'PRAGMA TablePathPrefix("{self.database}");\r\n'
        header += ''.join([self._datamode[value.get('mode', 'var')](key, value.get('val')) if isinstance(value, dict) else self._getDeclare(key, types[type(value)]) for key, value in payload.items()])
        return header

    def _getVar(self, key: str, value: str) -> str:
        return f'\r{key}={value};\n'

    def _getDeclare(self, key: str, vartype: str) -> str:
        return f'\rDECLARE {key} AS {vartype};\n'

    def _getWhere(self, key: str) -> str:
        return f'{key[1:]}={key}'

    def _getCustomType(self, payload: dict, key: str):
        custom_type, payload[key] = payload[key][1], payload[key][0]
        return custom_type

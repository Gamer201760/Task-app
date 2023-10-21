import ydb

from lib.ydb import database


async def create_table(session: ydb.Session):
    await session.create_table(
        f'{database}/task',
        ydb.TableDescription()
        .with_column(
            ydb.Column('id', ydb.PrimitiveType.String)
        )
        .with_column(
            ydb.Column('text', ydb.OptionalType(ydb.PrimitiveType.String))
        )
        .with_column(
            ydb.Column(
                'created_at',
                ydb.OptionalType(ydb.PrimitiveType.Int32))
        )
        .with_column(
            ydb.Column(
                'deadline',
                ydb.OptionalType(ydb.PrimitiveType.Int32))
        )
        .with_column(
            ydb.Column(
                'completed',
                ydb.OptionalType(ydb.PrimitiveType.Bool))
        )
        .with_primary_key('id')
    )

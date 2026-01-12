# app/api/v1/endpoints/trade.py

from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate


def create_trade(db: Session, *, user_id: str, payload: TradeCreate) -> Trade:
    t = Trade(
        user_id=user_id,

        # inputs
        balance_chf=payload.inputs.balance_chf,
        risk_pct=payload.inputs.risk_pct,
        symbol=payload.inputs.symbol,
        direction=payload.inputs.direction.value,
        entry_price=payload.inputs.entry_price,
        stop_distance=payload.inputs.stop_distance,
        stop_unit=payload.inputs.stop_unit.value,
        tp_r_multiple=payload.inputs.tp_r_multiple,
        lot_step=payload.inputs.lot_step,
        usdchf_rate=payload.inputs.usdchf_rate,
        tick_size=payload.inputs.tick_size,
        contract_size=payload.inputs.contract_size,

        # outputs
        sl_price=payload.outputs.sl_price,
        tp_price=payload.outputs.tp_price,
        risk_distance_price=payload.outputs.risk_distance_price,
        reward_distance_price=payload.outputs.reward_distance_price,
        lots=payload.outputs.lots,
        risk_chf=payload.outputs.risk_chf,
        reward_chf=payload.outputs.reward_chf,
        reward_to_risk=payload.outputs.reward_to_risk,
        value_per_unit_1lot_chf=payload.outputs.value_per_unit_1lot_chf,
        stop_value_1lot_chf=payload.outputs.stop_value_1lot_chf,
        exposure_units=payload.outputs.exposure_units,

        # journal
        note=payload.journal.note,
        status=payload.journal.status.value,
        opened_at=payload.journal.opened_at,
        closed_at=payload.journal.closed_at,
        realized_pnl_chf=payload.journal.realized_pnl_chf,
        realized_r_multiple=payload.journal.realized_r_multiple,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def list_trades_for_user(
    db: Session,
    *,
    user_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Trade]:
    stmt = (
        select(Trade)
        .where(Trade.user_id == user_id)
        .order_by(desc(Trade.created_at))
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt).all())



def get_trade_for_user(db: Session, *, user_id: str, trade_id: str) -> Trade | None:
    stmt = select(Trade).where(Trade.id == trade_id, Trade.user_id == user_id)
    return db.scalars(stmt).first()


def update_trade_for_user(db: Session, *, user_id: str, trade_id: str, payload: TradeUpdate) -> Trade | None:
    trade = get_trade_for_user(db, user_id=user_id, trade_id=trade_id)
    if not trade:
        return None

    data = payload.model_dump(exclude_unset=True)

    if "status" in data and data["status"] is not None:
        data["status"] = data["status"].value

    for k, v in data.items():
        setattr(trade, k, v)

    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

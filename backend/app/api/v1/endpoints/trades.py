# app/api/v1/endpoints/trades.py

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.crud.trade import create_trade, get_trade_for_user, list_trades_for_user, update_trade_for_user
from app.models.user import User
from app.schemas.trade import TradeCreate, TradeDetailOut, TradeSummaryOut, TradeUpdate, TradeInputs, TradeOutputs, TradeJournal

router = APIRouter(prefix="/trades", tags=["trades"])


def _to_detail_out(t) -> TradeDetailOut:
    return TradeDetailOut(
        id=t.id,
        user_id=t.user_id,
        created_at=t.created_at,
        updated_at=t.updated_at,
        inputs=TradeInputs(
            balance_chf=t.balance_chf,
            risk_pct=t.risk_pct,
            symbol=t.symbol,
            direction=t.direction,
            entry_price=t.entry_price,
            stop_distance=t.stop_distance,
            stop_unit=t.stop_unit,
            tp_r_multiple=t.tp_r_multiple,
            lot_step=t.lot_step,
            usdchf_rate=t.usdchf_rate,
            tick_size=t.tick_size,
            contract_size=t.contract_size,
        ),
        outputs=TradeOutputs(
            sl_price=t.sl_price,
            tp_price=t.tp_price,
            risk_distance_price=t.risk_distance_price,
            reward_distance_price=t.reward_distance_price,
            lots=t.lots,
            risk_chf=t.risk_chf,
            reward_chf=t.reward_chf,
            reward_to_risk=t.reward_to_risk,
            value_per_unit_1lot_chf=t.value_per_unit_1lot_chf,
            stop_value_1lot_chf=t.stop_value_1lot_chf,
            exposure_units=t.exposure_units,
        ),
        journal=TradeJournal(
            note=t.note,
            status=t.status,
            opened_at=t.opened_at,
            closed_at=t.closed_at,
            realized_pnl_chf=t.realized_pnl_chf,
            realized_r_multiple=t.realized_r_multiple,
        ),
    )


def _to_summary_out(t) -> TradeSummaryOut:
    return TradeSummaryOut(
        id=t.id,
        created_at=t.created_at,
        symbol=t.symbol,
        direction=t.direction,
        status=t.status,
        outputs=TradeOutputs(
            sl_price=t.sl_price,
            tp_price=t.tp_price,
            risk_distance_price=t.risk_distance_price,
            reward_distance_price=t.reward_distance_price,
            lots=t.lots,
            risk_chf=t.risk_chf,
            reward_chf=t.reward_chf,
            reward_to_risk=t.reward_to_risk,
            value_per_unit_1lot_chf=t.value_per_unit_1lot_chf,
            stop_value_1lot_chf=t.stop_value_1lot_chf,
            exposure_units=t.exposure_units,
        ),
    )


@router.post("", response_model=TradeDetailOut, status_code=status.HTTP_201_CREATED)
def create_planned_trade(
    payload: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trade = create_trade(db, user_id=current_user.id, payload=payload)
    return _to_detail_out(trade)


@router.get("", response_model=list[TradeSummaryOut])
def list_my_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = list_trades_for_user(db, user_id=current_user.id)
    return [_to_summary_out(t) for t in trades]


@router.get("/{trade_id}", response_model=TradeDetailOut)
def get_my_trade(
    trade_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trade = get_trade_for_user(db, user_id=current_user.id, trade_id=trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return _to_detail_out(trade)


@router.patch("/{trade_id}", response_model=TradeDetailOut)
def patch_my_trade(
    trade_id: str,
    payload: TradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trade = update_trade_for_user(db, user_id=current_user.id, trade_id=trade_id, payload=payload)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return _to_detail_out(trade)

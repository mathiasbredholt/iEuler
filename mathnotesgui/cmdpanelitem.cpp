#include "cmdpanelitem.h"

CmdPanelItem::CmdPanelItem(int index, QString value)
{
    this->index = index;
    setText(value);
    setHover(index == 0);
}

void CmdPanelItem::setHover(bool hover)
{
    if (hover) {
        setStyleSheet("QLabel { background: #DDD; padding: 2px }");
    } else {
        setStyleSheet("QLabel { background: none; padding: 2px }");
    }
}


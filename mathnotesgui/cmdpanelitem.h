#ifndef CMDPANELITEM_H
#define CMDPANELITEM_H

#include <QWidget>
#include <QLabel>

class CmdPanelItem : public QLabel
{
    Q_OBJECT
public:
    explicit CmdPanelItem(int index, QString value = "");
    void setHover(bool hover);
    int index;

private:
};

#endif // CMDPANELITEM_H

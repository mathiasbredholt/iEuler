#ifndef CMDPANEL_H
#define CMDPANEL_H

#include <QWidget>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QEvent>
#include <QKeyEvent>
#include <QDebug>

#include "cmdpanelitem.h"

class CmdPanel : public QWidget
{
    Q_OBJECT
public:
    explicit CmdPanel(QWidget *parent = 0);

private:
    QLineEdit *cmdline;
    int focusIndex;
    int itemCount;
    bool eventFilter(QObject *object, QEvent *event);

signals:

public slots:

protected:
  void showEvent(QShowEvent *e);
};

#endif // CMDPANEL_H

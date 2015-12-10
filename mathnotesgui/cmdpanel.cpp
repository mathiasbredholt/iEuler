#include "cmdpanel.h"

CmdPanel::CmdPanel(QWidget *parent) : QWidget(parent)
{
    hide();
    focusIndex = 0;
    itemCount = 0;

    setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Preferred);
    setFixedWidth(128);
    setStyleSheet("QWidget { background: #EEE; }");
    setContentsMargins(0, 0, 0, 0);


    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setAlignment(Qt::AlignTop);
    layout->setContentsMargins(0, 8, 13, 0);

    cmdline = new QLineEdit(this);
    cmdline->setStyleSheet("QLineEdit { background: #DDD; border: none; }");
    cmdline->setAttribute(Qt::WA_MacShowFocusRect, 0);
    cmdline->installEventFilter(this);
    layout->addWidget(cmdline);

    layout->addWidget(new CmdPanelItem(itemCount, "Evaluate"));
    itemCount++;

    layout->addWidget(new CmdPanelItem(itemCount, "Save file"));
    itemCount++;

    layout->addWidget(new CmdPanelItem(itemCount, "Open file"));
    itemCount++;

    layout->addWidget(new CmdPanelItem(itemCount, "Quit"));
    itemCount++;
}

bool CmdPanel::eventFilter(QObject *object, QEvent *event)
{
    if (event->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);

        if (keyEvent->key() == Qt::Key_Return) {
            QList<CmdPanelItem *> items = this->parent()->findChildren<CmdPanelItem *>();
            qDebug() << items.at(focusIndex)->text();
            return true;
        } else if (keyEvent->key() == Qt::Key_Up) {
            if (focusIndex > 0) {
                focusIndex--;

                QList<CmdPanelItem *> items = this->parent()->findChildren<CmdPanelItem *>();

                QListIterator<CmdPanelItem *> i(items);
                while (i.hasNext()) {
                    CmdPanelItem *item = i.next();
                    item->setHover(focusIndex == item->index);
                }

            }
            return true;
        } else if (keyEvent->key() == Qt::Key_Down) {
            if (focusIndex < itemCount - 1) {
                focusIndex++;

                QList<CmdPanelItem *> items = this->findChildren<CmdPanelItem *>();

                QListIterator<CmdPanelItem *> i(items);
                while (i.hasNext()) {
                    CmdPanelItem *item = i.next();
                    item->setHover(focusIndex == item->index);
                }
            }
            return true;
        }
    }

    return false;
}

void CmdPanel::showEvent(QShowEvent *e)
{
    cmdline->setFocus();
}

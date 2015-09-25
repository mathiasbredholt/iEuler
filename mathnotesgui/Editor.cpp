#include "Editor.h"

Editor::Editor(QWidget *parent) : QLineEdit(parent)
{
this->setStyleSheet("QLineEdit { color: white; border: none; }");
this->installEventFilter(this);
}

bool Editor::eventFilter(QObject *object, QEvent *e)
{
    if (object == this && e->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(e);
        if (keyEvent->key() == Qt::Key_Return) {
            qDebug(this->text().toLatin1());
            return true;
        }
    }
    return false;
}

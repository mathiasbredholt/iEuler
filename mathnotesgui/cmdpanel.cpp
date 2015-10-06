#include "cmdpanel.h"

CmdPanel::CmdPanel(QWidget *parent) : QFrame(parent)
{
hide();
setStyleSheet("QFrame { background: #EEE; }");
QVBoxLayout *layout = new QVBoxLayout(this);
layout->setAlignment(Qt::AlignTop);

cmdline = new QLineEdit(this);
layout->addWidget(cmdline);

QLabel *item1 = new QLabel("Evaluate");
layout->addWidget(item1);

QLabel *item2 = new QLabel("Quit");
layout->addWidget(item2);
}

void CmdPanel::showEvent(QShowEvent *e)
{
    cmdline->setFocus();
}

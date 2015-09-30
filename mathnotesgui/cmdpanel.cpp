#include "cmdpanel.h"

CmdPanel::CmdPanel(QWidget *parent) : QFrame(parent)
{
hide();
setStyleSheet("QFrame { background: #EEE; }");
QVBoxLayout *layout = new QVBoxLayout(this);
layout->setAlignment(Qt::AlignTop);

cmdline = new QLineEdit(this);
layout->addWidget(cmdline);
}

void CmdPanel::showEvent(QShowEvent *e)
{
    cmdline->setFocus();
}

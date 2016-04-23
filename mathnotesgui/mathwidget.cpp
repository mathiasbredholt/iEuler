#include "mathwidget.h"

MathWidget::MathWidget(QWidget *parent) : QLabel(parent)
{
    setFocusPolicy(Qt::NoFocus);
}

void MathWidget::loadPlot(QString path)
{
    QPixmap src = QPixmap(path);
    setPixmap(src);
}

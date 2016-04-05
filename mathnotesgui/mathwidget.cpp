#include "mathwidget.h"

MathWidget::MathWidget(QWidget *parent) : QLabel(parent)
{
}

void MathWidget::loadPlot(QString path)
{
    QPixmap src = QPixmap(path);
    setPixmap(src);
}

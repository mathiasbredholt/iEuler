#ifndef MATHWIDGET_H
#define MATHWIDGET_H

#include <QLabel>

class MathWidget : public QLabel
{
    Q_OBJECT
public:
    explicit MathWidget(QWidget *parent = 0);
    QString latexString;
    void loadPlot(QString path);

public slots:

};

#endif // MATHWIDGET_H

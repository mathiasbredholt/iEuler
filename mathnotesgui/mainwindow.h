#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "ui_mainwindow.h"
#include "codeinput.h"
#include <QLabel>
#include <QSizePolicy>
#include <QProcess>
#include<QtCore/QFile>
#include<QtCore/QTextStream>
#include <QProcess>
#include <QThread>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

    void createNewCodeLine();

private slots:
    void evaluateCode(QString inputString);
    void deleteCode(CodeInput* target);
};

#endif // MAINWINDOW_H

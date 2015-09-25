#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->content->layout()->setAlignment(Qt::AlignTop);
    this->createNewCodeLine();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::evaluateCode(QString inputString)
{
//    qDebug("cd ../.. && python3 start.py " + inputString.toLatin1());
    QProcess p;
    QStringList params;

//    p.setWorkingDirectory("../../");

    params << "start.py" << inputString;
    p.start("/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4", params);
    p.waitForFinished(-1);

    p.start("convert -density 300 mathnotes.pdf mathnotes.png");
    p.waitForFinished(-1);

    QLabel* img = new QLabel("<img src='mathnotes.png' />");
    img->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    ui->content->layout()->addWidget(img);
    this->createNewCodeLine();
}

void MainWindow::deleteCode(CodeInput* target)
{
    ui->content->setFocus();
    ui->content->layout()->removeWidget(target);
    delete target;
}


void MainWindow::createNewCodeLine()
{
    CodeInput* ci = new CodeInput();
    ui->content->layout()->addWidget(ci);
    ci->setFocus();
    QObject::connect(ci, SIGNAL(evaluateCode(QString)), this, SLOT(evaluateCode(QString)));
    QObject::connect(ci, SIGNAL(deleteCode(CodeInput*)), this, SLOT(deleteCode(CodeInput*)));
}

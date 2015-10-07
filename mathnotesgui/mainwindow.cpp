#include "mainwindow.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    installEventFilter(this);

    numberOfLines = 0;
    cmdpanel = new CmdPanel(this);

    ui->container->layout()->addWidget(cmdpanel);
    ui->content->layout()->setAlignment(Qt::AlignTop);

    createNewCodeLine();

    initSubprocess();
}

void MainWindow::initSubprocess()
{
    proc = new QProcess(this);
    proc->start("python3 start.py -gui");
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
}

void MainWindow::readStandardOutput()
{
    int line = QString(proc->readAllStandardOutput()).toInt();
    // get line number from python
     emit outputReady(line)
//    emit outputReady(0);
}

void MainWindow::readStandardError()
{
    qDebug() << proc->readAllStandardError();
}


MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::evaluateCode(CodeInput* target, QString inputString)
{
    proc->write(inputString.toLatin1()+"\n");
    if (((Group*) target->parent())->index == numberOfLines-1) {
        createNewCodeLine();
    }
}

void MainWindow::deleteGroup(QWidget *target)
{
    if (numberOfLines > 1) {
        focusPreviousChild();
        ui->content->layout()->removeWidget(target);
        delete target;
        numberOfLines--;
    }
}


void MainWindow::createNewCodeLine()
{
    Group* gp = new Group(this, numberOfLines);
    ui->content->layout()->addWidget(gp);
    gp->input->setFocus();
    connect(gp->input, SIGNAL(evaluateCode(CodeInput*, QString)), this, SLOT(evaluateCode(CodeInput*, QString)));
    connect(gp->input, SIGNAL(deleteGroup(QWidget*)), this, SLOT(deleteGroup(QWidget*)));
    connect(gp->input, SIGNAL(arrowsPressed(bool)), this, SLOT(arrowsPressed(bool)));
    connect(this, SIGNAL(outputReady(int)), gp, SLOT(outputReady(int)));
    numberOfLines++;
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

void MainWindow::arrowsPressed(bool upArrowPressed)
{
    int index = ((Group*) focusWidget()->parent())->index;
    if (upArrowPressed) {
        if (index > 0) focusPreviousChild();
    } else {
        if (index < numberOfLines-1) focusNextChild();
    }
}

void MainWindow::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_Escape) {
        cmdpanel->hide();
    }
}

#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    cmdpanel = new CmdPanel(this);
    ui->container->layout()->addWidget(cmdpanel);

    ui->content->layout()->setAlignment(Qt::AlignTop);

    this->createNewCodeLine();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::evaluateCode(CodeInput* target, QString inputString)
{
    QProcess p;
    QStringList params;

    params << "start.py" << inputString;
    p.start("python3", params);
    p.waitForFinished(-1);

    p.start("convert -density 300 mathnotes.pdf mathnotes.png");
    p.waitForFinished(-1);

    emit outputReady();

    createNewCodeLine();
}

void MainWindow::deleteGroup(Group* target)
{
    ui->content->setFocus();
    ui->content->layout()->removeWidget(target);
    delete target;
}


void MainWindow::createNewCodeLine()
{
    Group* gp = new Group();
    ui->content->layout()->addWidget(gp);
    gp->input->setFocus();
    QObject::connect(gp->input, SIGNAL(evaluateCode(CodeInput*, QString)), this, SLOT(evaluateCode(CodeInput*, QString)));
    QObject::connect(gp, SIGNAL(deleteGroup(Group*)), this, SLOT(deleteGroup(Group*)));
    QObject::connect(this, SIGNAL(outputReady()), gp, SLOT(outputReady()));
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

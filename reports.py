import HTML
import AdminConfig
import AdminTask

def writeQueuesByScope(scopeIds, qParams, tableId):
  for s in scopeIds :
    try :
      queues = AdminTask.listWMQQueues(s).splitlines()
      scope = s.split('|')[0].split('(')[1]
      for q in queues :
        tArgs = []
        for p in qParams :
          paramValue = AdminConfig.showAttribute(q,p)
          tArgs.append(paramValue)
        tArgs.append(scope)
        tableId.rows.append(tArgs)
    except :
      print sys.exc_info()
 
QUEUE_HTML_FILE = 'Queues.html'
queuesFile = open(QUEUE_HTML_FILE, 'w')
            
queueT = HTML.Table(header_row=['Name', 'JNDI name', 'MQ Queue manager', 'MQ Queue name', 'Scope'])
queueParams = ["name", "jndiName", "baseQueueManagerName", "baseQueueName"]

cell = AdminConfig.getid('/Cell:/').splitlines()
nodes = AdminConfig.getid('/Node:/').splitlines()
servers = AdminConfig.getid('/Server:/').splitlines()

writeQueuesByScope(servers, queueParams, queueT)

htmlcode = str(queueT)
queuesFile.write(htmlcode)
queuesFile.write('<p>')

dbT = HTML.Table(header_row=['Name', 'JNDI name', 'Provider', 'JAAS Alias', 'Scope'])
dbParams = ['name', 'jndiName', 'provider', 'authDataAlias']



'''
Создание страницы с jvm аргументами
'''




for s in servers :
  servName = s.split('(')[0]
  nodeName = s.split('/')[3]
  args = '[-nodeName ' + nodeName + ' -serverName ' + servName + ']'
  paramValue = AdminTask.showJVMProperties(args)

'''
datasourcesId = AdminConfig.list('DataSource').splitlines()
for i in datasourcesId :
    dsScope = i.split('(')[1].split('|')[0]
    writeParamsToHTML(i, dsScope, dbParams, dbT)
'''
queuesFile.close()

INDEX_HTML_FILE = 'Index.html' 
indexFile = open(INDEX_HTML_FILE, 'w')
htmlcode = HTML.link('Queues', '.\Queues.html')
indexFile.write(htmlcode)
indexFile.write('<p>')
indexFile.close()
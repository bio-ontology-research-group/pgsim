@Grab(group='com.github.sharispe', module='slib-sml', version='0.9.1')
@Grab(group='org.codehaus.gpars', module='gpars', version='1.1.0')

import java.net.*
import org.openrdf.model.vocabulary.*
import slib.sglib.io.loader.*
import slib.sml.sm.core.metrics.ic.utils.*
import slib.sml.sm.core.utils.*
import slib.sglib.io.loader.bio.obo.*
import org.openrdf.model.URI
import slib.graph.algo.extraction.rvf.instances.*
import slib.sglib.algo.graph.utils.*
import slib.utils.impl.Timer
import slib.graph.algo.extraction.utils.*
import slib.graph.model.graph.*
import slib.graph.model.repo.*
import slib.graph.model.impl.graph.memory.*
import slib.sml.sm.core.engine.*
import slib.graph.io.conf.*
import slib.graph.model.impl.graph.elements.*
import slib.graph.algo.extraction.rvf.instances.impl.*
import slib.graph.model.impl.repo.*
import slib.graph.io.util.*
import slib.graph.io.loader.*
import slib.graph.algo.extraction.rvf.DescendantEngine;
import slib.graph.algo.accessor.GraphAccessor;

import groovyx.gpars.GParsPool



def factory = URIFactoryMemory.getSingleton()

def getGeneOntology = {

  URI graph_uri = factory.getURI("http://go/")
  factory.loadNamespacePrefix("GO", graph_uri.toString())
  G graph = new GraphMemory(graph_uri)

  // Load OBO file to graph "gene_ontology_ext.obo"
  GDataConf goConf = new GDataConf(GFormat.OBO, "data/gene_ontology_ext.obo")
  GraphLoaderGeneric.populate(goConf, graph)

  // Add virtual root for 3 subontologies__________________________________
  URI functionsRoot = factory.getURI("http://go/0003674")
  DescendantEngine descGetter = new DescendantEngine(graph)
  Set<URI> functions = new HashSet<URI>();
  Queue<URI> q = new LinkedList<URI>();
  q.add(functionsRoot);
  functions.add(functionsRoot);
  while(!q.isEmpty()) {
    URI v = q.poll();
    Set<URI> childs = graph.getV(v, descGetter.getWalkConstraint());
    for (URI child: childs) {
      if (!functions.contains(child)) {
        q.add(child);
        functions.add(child);
      }
    }
  }
  Set<URI> others = new HashSet<URI>(graph.getV());
  others.removeAll(functions);
  graph.removeV(others);

  GAction rooting = new GAction(GActionType.REROOTING);
  rooting.addParameter("root_uri", functionsRoot.stringValue());
  GraphActionExecutor.applyAction(factory, rooting, graph);

  return graph
}


graph = getGeneOntology()

SM_Engine engine = new SM_Engine(graph)

ICconf icConf = new IC_Conf_Topo("Sanchez", SMConstants.FLAG_ICI_SANCHEZ_2011);
SMconf smConf = new SMconf("Lin", SMConstants.FLAG_SIM_PAIRWISE_DAG_NODE_LIN_1998);
smConf.setICconf(icConf);

Set<URI> classes = GraphAccessor.getClasses(graph);
URI[] gos = classes.toArray(new URI[classes.size()]);
def n = gos.length;
Double[][] sims = new Double[n][n];
for (int i = 0; i < n; i++) {
  for (int j = i; j < n; j++) {
    sims[i][j] = engine.compare(smConf, gos[i], gos[j]);
  }
}

// GParsPool.withPool {
//   result.eachParallel { val ->
//     def i = val[0].toInteger()
//     for (j = i; j < 5000; j++) {
//       result[i][j] = engine.compare(
//               smConfGroupwise,
//               smConfPairwise,
//               genes[i].getAnnotations(),
//               genes[j].getAnnotations())
//     }
//     c += 1
//     println c
//   }
// }


def fout = new PrintWriter(new BufferedWriter(
  new FileWriter("functions.txt")));
for (i = 0; i < n; i++) {
  fout.print(gos[i])
  for (j = 0; j < n; j++) {
    if (i < j) {
      fout.printf(" %.3f", sims[i][j]);
    } else {
      fout.printf(" %.3f", sims[j][i]);
    }
  }
  fout.println();
}

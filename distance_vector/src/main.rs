use std::collections::HashMap;

type FinDist = u32;
#[derive(Copy, Clone, Hash, Debug, Eq, PartialEq)]
enum Dist {
    Fin(FinDist),
    Inf,
}
impl PartialOrd for Dist {
    fn ge(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Inf, Self::Inf) => true,
            (Self::Inf, Self::Fin(_)) => true,
            (Self::Fin(_), Self::Inf) => false,
            (Self::Fin(val), Self::Fin(other)) => val.ge(other)
        }
    }
    fn gt(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Inf, Self::Inf) => false,
            (Self::Inf, Self::Fin(_)) => true,
            (Self::Fin(_), Self::Inf) => false,
            (Self::Fin(val), Self::Fin(other)) => val.gt(other)
        }
    }
    fn le(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Inf, Self::Inf) => true,
            (Self::Inf, Self::Fin(_)) => false,
            (Self::Fin(_), Self::Inf) => true,
            (Self::Fin(val), Self::Fin(other)) => val.le(other)
        }
    }
    fn lt(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Inf, Self::Inf) => false,
            (Self::Inf, Self::Fin(_)) => false,
            (Self::Fin(_), Self::Inf) => true,
            (Self::Fin(val), Self::Fin(other)) => val.lt(other)
        }
    }
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        use std::cmp::Ordering::*;
        if self == other {
            Some(Equal)
        } else if self.gt(other) {
            Some(Greater)
        } else {
            Some(Less)
        }
    }
}
impl std::ops::Add for Dist {
    type Output = Dist;
    fn add(self, rhs: Self) -> Self::Output {
        match (self, rhs) {
            (Self::Inf, Self::Inf) => Self::Inf,
            (Self::Inf, Self::Fin(_)) => Self::Inf,
            (Self::Fin(_), Self::Inf) => Self::Inf,
            (Self::Fin(val), Self::Fin(other)) => Self::Fin(val + other),
        }
    }
}

type NodeId = char;
type DistVec = HashMap<NodeId, Dist>;
#[derive(Clone, Debug, Eq, PartialEq)]
struct Node {
    id: NodeId,
    neighbors: HashMap<NodeId, FinDist>,
    dv: DistVec,
    new_dv: DistVec,
}
impl Node {
    fn new(id: NodeId, neighbors: HashMap<NodeId, FinDist>, all_nodes: &[NodeId]) -> Self {
        let dv = all_nodes
                .iter()
                .map(|id| match neighbors.get(id) {
                    Some(dist) => (*id, Dist::Fin(*dist)),
                    None => (*id, Dist::Inf),
                })
                .collect();
        Node {
            id,
            neighbors,
            dv,
            new_dv: HashMap::new(),
        }
    }
    fn receive_dv(&mut self, dv: &DistVec, neighbor: NodeId) {
        self.new_dv = self.dv.clone();
        for (id, dist) in dv {
            // let new_dist = 
        }
    }
    fn update_dv(&mut self) {
        self.dv = std::mem::take(&mut self.new_dv);
    }
}
type Graph = Vec<Node>;

fn main() {
    println!("Hello, world!");
}

(* given a list with at least four elements, find the four largest ones in
one pass *)


use "/Users/iev/.bin/sml_prelude/prelude.sml";

fun update (new, old as (x,y,z,w)) =
    case (new > x, new > y, new > z, new > w)
     of (true, _, _, _) => (new, y, z, w)
      | (_, true, _, _) => (x, new, z, w)
      | (_, _, true, _) => (x, y, new, w)
      | (_, _, _, true) => (x, y, z, new)
      | _ => old

fun maxfour (l : int list) : int * int * int * int =
    let
      val a :: b :: c :: d :: rest = l
    in
      foldr update (a,b,c,d) rest
    end

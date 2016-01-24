(* given a list with at least four elements, find the four largest ones in
one pass *)


use "/Users/iev/.bin/sml_prelude/prelude.sml";

(* this was my first attempt *)
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

(* it's totally wrong! in update i'm missing all kinds of comparisons
   because i'm making stupid assumptions about the relationship between the
   next number from the list, new, and any of the existing
   best-guess-maxes

   this is obfuscated in the single-max case because there's only one
   possible comparison, but it goes up by like catalan i think, so it's
   nasty to write out hard coded. also that fixes k, which is silly when
   it's going to be a constant.
*)


(* single max *)
fun max [] = raise Fail ""
  | max (a :: l) = foldr (fn (x,y) => if x > y then x else y) a l

(* flip int.compare to sort things in reverse; forget if there's a faster
   way to do this *)
fun ic p =
    case Int.compare p
     of LESS => GREATER
      | GREATER => LESS
      | x => x


fun update2 (new , old as (m1, m2)) : int * int =
    let
      val a :: b :: _ = sort ic [new, m1, m2]
    in
      (a,b)
    end

fun max2 (l : int list) =
    let
      val a :: b :: rest = l
      (* needed this for the hot second there when i had the right
         comparisons but not sort *)

      (* val p = if a < b then (b,a) else (a,b) *)
    in
      foldr update2 (a,b) rest
    end

(* find the k largest things in an unordered list of length n in O(n) *)
fun updatek k (new : int , prev : int list) : int list =
    List.take (sort ic (new :: prev), k)

(* this sort is not really important. it's actually almost more of an aid
   to readability. for one thing, it's O(k lg k) and we take k to be
   constant, so the over running time is O(n * k lg k) which is still
   O(n). intuitively, it's just a faster way to write down all the
   comparisons you'd need to do to update that tuple of maxes-so-far
   without missing any. really doesn't even add any over doing it out by
   hand; there's a minimum number of comparisons you need to do to get the
   right tuple and it's ~lg.
   *)

(* k has to be <= length l; you can't take the k biggest elements if there
   aren't k elements. could imagine a version that did "no more than k" or
   returned an option or something but that's not important. *)

fun maxk k (l : int list) : int list =
    if (length l < k) then raise Fail ""
    else
      let
        val (first_k,rest) = (List.take(l,k), List.drop(l,k))
      in
        sort ic (foldr (updatek k) first_k rest)
      end

(* run maxk on all reasonable k up to n on all permutations of lists of the
   numbers 0..n *)
fun test n =
    let
      val perms = permutations (List.tabulate(n, fn x => x))
    in
      List.tabulate (n+1, fn x => uniqc (op=) (map (maxk x) perms))
    end

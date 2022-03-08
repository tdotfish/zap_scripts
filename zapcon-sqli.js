var attacks = [
	"'",
	"\"",
	";",
	"';"
]
function scan(as, msg, param, value) {
	for (i = 0; i < attacks.length; i++) {
		new_msg = msg.cloneRequest();
		attack1 = attacks[i]
		print("attack1 = ",attack1);
		as.setParam(new_msg, param, value + attack1);
		as.sendAndReceive(new_msg, false, false);
	}
}
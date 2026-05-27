Interceptor.attach(ptr("0x19976b4e4"), {
    onEnter: function(args) {
        this.buf = args[1];
        this.len = args[2].toInt32();
    },
    onLeave: function(retval) {
        if (this.len > 5) {
            var bytes = new Uint8Array(this.buf.readByteArray(this.len));
            var hex = Array.from(bytes).map(b => b.toString(16).padStart(2,'0')).join(' ');
            var text = "";
            try { text = this.buf.readUtf8String(this.len); } catch(e) {}
            
            if (text.includes("grpc") || text.includes(":method") || 
                text.includes("PRI *") || bytes[0] === 0x50) {
                console.log("\n[OUT] " + this.len + " bytes");
                console.log(hex.substring(0, 100));
                if (text.length > 0) console.log("[TEXT] " + text.substring(0, 200));
            }
        }
    }
});

Interceptor.attach(ptr("0x19976b1a0"), {
    onEnter: function(args) {
        this.buf = args[1];
    },
    onLeave: function(retval) {
        var len = retval.toInt32();
        if (len > 5) {
            var bytes = new Uint8Array(this.buf.readByteArray(len));
            var hex = Array.from(bytes).map(b => b.toString(16).padStart(2,'0')).join(' ');
            var text = "";
            try { text = this.buf.readUtf8String(len); } catch(e) {}
            
            if (text.includes("grpc") || text.includes(":status") || len > 50) {
                console.log("\n[IN] " + len + " bytes");
                console.log(hex.substring(0, 100));
                if (text.length > 0) console.log("[TEXT] " + text.substring(0, 200));
            }
        }
    }
});

console.log("[*] Ready - تفاعل مع التطبيق الآن");

import sys

# Global variables
SYMTAB = []
OPTAB = []

class SYMBOL:
    def __init__( self, name, addr ):
        self.name = name
        self.addr = addr

class OPCODE:
    def __init__( self, opcode, _format ):
        self.opcode = opcode
        self._format = _format

def OPTAB_init():
    OPTAB.append( OPCODE( 'ADD'  , 0x18 ) )
    OPTAB.append( OPCODE( 'STA'  , 0x0C ) )
    OPTAB.append( OPCODE( 'STL'  , 0x14 ) )
    OPTAB.append( OPCODE( 'STX'  , 0x10 ) )
    OPTAB.append( OPCODE( 'LDA'  , 0x00 ) )
    OPTAB.append( OPCODE( 'LDB'  , 0x68 ) )
    OPTAB.append( OPCODE( 'LDT'  , 0x74 ) )
    OPTAB.append( OPCODE( 'JSUB' , 0x48 ) )
    OPTAB.append( OPCODE( 'RSUB' , 0x4C ) )
    OPTAB.append( OPCODE( 'COMP' , 0x28 ) )
    OPTAB.append( OPCODE( 'COMPR', 0xA0 ) )
    OPTAB.append( OPCODE( 'J'    , 0x3C ) )
    OPTAB.append( OPCODE( 'JEQ'  , 0x30 ) )
    OPTAB.append( OPCODE( 'JLT'  , 0x38 ) )
    OPTAB.append( OPCODE( 'TIXR' , 0xB8 ) )
    OPTAB.append( OPCODE( 'CLEAR', 0xB4 ) )
    OPTAB.append( OPCODE( 'TD'   , 0xE0 ) )
    OPTAB.append( OPCODE( 'RD'   , 0xD8 ) )
    OPTAB.append( OPCODE( 'WD'   , 0xDC ) )
    OPTAB.append( OPCODE( 'STCH' , 0x54 ) )
    OPTAB.append( OPCODE( 'LDCH' , 0x50 ) )
    return

def OPTAB_print():
    print( 'OPTAB:' )
    for e in OPTAB:
        print( e.opcode, '\t', e._format )
    print( '------------', end = '\n\n' )

def SYMTAB_print():
    print( 'SYMTAB:' )
    for e in SYMTAB:
        print( e.name, '\t', e.addr )
    print( '------------', end = '\n\n' )

def formObjectCode( opcode, operand ):
    return

def formObjectCodeConstant( opcode, operand ):
    return

def PASS1( raw, startAddr, programName, LOCCTR, ProgramLength ):
    """ First Line """
    s = raw.getline()
    if not s:
        print( 'This is a blank file :(' )
        exit(0)
    if s[1] == 'START':             # else case is skipped since declaration has done the task
        programName = s[0]
        startAddr = int( s[2] )     # s[2] may be in hex string
        LOCCTR = startAddr

    """ Middle Lines """
    while True:
        s = raw.getline()
        if s[1] == 'END':
            break
        if """ This is not a comment line """:
            # ", X" case
            if s[-2][-1] == ',' && s[-1] == 'X':
                s[-2].append('X')
                s.pop(-1)

            # Label, format s into length-3 list
            if len(s) == 3:
                if """s[0] in SYMTAB""":
                    print( 'Error: Duplicate Symbol Declaration: ', s[0] )
                    exit(-1)
                else:
                    SYMTAB.append( SYMBOL( s[0], LOCCTR ) )
            elif len(s) == 2:
                s.insert( 0, "" )
            else:
                print( 'Error in this statement: ', s )
                exit(-1)

            # Modify LOCCTR
            op = ""
            if s[1][0] == '+':
                op = s[1][1:]
            else:
                op = s[1]

            if """ op in OPTAB """:
                LOCCTR += """ op.format"""
            elif s[1] == 'WORD':
                LOCCTR += 3
            elif s[1] == 'BYTE':
                LOCCTR += 1
            elif s[1] == 'RESW':
                LOCCTR += """ number of operand """
            elif s[1] == 'RESB':
                LOCCTR += """ number of operand """
            else:
                print( 'Error: ', s[1], ' is not a legal OPCODE', sep='', end='\n' )
                exit(-1)
    ProgramLength = LOCCTR - startAddr
    return

def PASS2( raw, startAddr, programName, LOCCTR, ProgramLength ):
    objCode = open( "objCode.txt", "w" )

    """ First Line """
    s = raw.getline()
    if not s:
        print( 'This is a blank file :(' )
        exit(0)
    if s[1] == 'START':             # else case is skipped since declaration has done the task
        """ Header """
        HRecord = "H" + programName + str( startAddr ) + str( ProgramLength )   # Format the last two parameter is required
        objCode.write( HRecord )

    TRecord = "T" + str( LOCCTR ) + "00"    # how to write starting addr and length

    """ Middle Lines """
    while True:
        s = raw.getline()
        if s[1] == 'END':
            break
        if """ This is not a comment line """:
            # ", X" case
            if s[-2][-1] == ',' && s[-1] == 'X':
                s[-2].append('X')
                s.pop(-1)

            # Format s into length-3 list
            if len(s) == 2:
                s.insert( 0, "" )

            if """ s[1] in OPTAB """ :
                formObjectCode( s[1], s[2] )
            elif s[1] == 'BYTE' or s[1] == 'WORD':
                """ Convert Constant to ObjectCode """
                formObjectCodeConstant( s[1], s[2] )

            # Over text record range
            if """ It's time to create a new T record """:
                objCode.write( TRecord )
                TRecord = "T" + str( LOCCTR ) + "00"    # how to write starting addr and length
            

    ERecord = "E" + str( startAddr )
    objCode.write( ERecord )

    objCode.close()
    return

def main():
    # Variables I need
    OPTAB_init()
    startAddr = 0
    programName = ""
    LOCCTR = 0
    ProgramLength = 0

    asmFile = sys.argv[1]
    raw = open( asmFile, 'r' )

    PASS1( raw, startAddr, programName, LOCCTR, ProgramLength )

    """ Test: OP table and Symbol Table """
    OPTAB_print()
    SYMTAB_print()

    raw.seek(0)     # Back to the file beginning
    
    PASS2( raw, startAddr, programName, LOCCTR, ProgramLength )

    raw.close()
    
if __name__ == "__main__":
    main()

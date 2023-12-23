import sys

# Global variables
SYMTAB_name = []
SYMTAB_addr = []
OPTAB_name  = []
OPTAB_code  = []

def OPTAB_init():
    OPTAB_name.append( 'ADD' )
    OPTAB_code.append( 0x18 )
    OPTAB_name.append( 'STA' )
    OPTAB_code.append( 0x0C )
    OPTAB_name.append( 'STL' )
    OPTAB_code.append( 0x14 )
    OPTAB_name.append( 'STX' )
    OPTAB_code.append( 0x10 )
    OPTAB_name.append( 'LDA' )
    OPTAB_code.append( 0x00 )
    OPTAB_name.append( 'LDB' )
    OPTAB_code.append( 0x68 )
    OPTAB_name.append( 'LDT' )
    OPTAB_code.append( 0x74 )
    OPTAB_name.append( 'JSUB')
    OPTAB_code.append( 0x48 )
    OPTAB_name.append( 'RSUB')
    OPTAB_code.append( 0x4C )
    OPTAB_name.append( 'COMP')
    OPTAB_code.append( 0x28 )
    OPTAB_name.append( 'COMPR' )    # format 2
    OPTAB_code.append( 0xA0 )       # format 2
    OPTAB_name.append( 'J'   )
    OPTAB_code.append( 0x3C )
    OPTAB_name.append( 'JEQ' )
    OPTAB_code.append( 0x30 )
    OPTAB_name.append( 'JLT' )
    OPTAB_code.append( 0x38 )
    OPTAB_name.append( 'TIXR')      # format 2
    OPTAB_code.append( 0xB8 )       # format 2
    OPTAB_name.append( 'CLEAR' )    # format 2
    OPTAB_code.append( 0xB4 )       # format 2
    OPTAB_name.append( 'TD'  )
    OPTAB_code.append( 0xE0 )
    OPTAB_name.append( 'RD'  )
    OPTAB_code.append( 0xD8 )
    OPTAB_name.append( 'WD'  )
    OPTAB_code.append( 0xDC )
    OPTAB_name.append( 'STCH')
    OPTAB_code.append( 0x54 )
    OPTAB_name.append( 'LDCH')
    OPTAB_code.append( 0x50 )
    return

def OPTAB_print():
    print( 'OPTAB:' )
    print( '-------------------------------------------------', end = '\n' )
    for i in range( len( OPTAB_name ) ):
        print( '|\t', OPTAB_name[i], '\t\t|\t', '{:02X}'.format( OPTAB_code[i] ), '\t\t|', sep='' )
    print( '-------------------------------------------------', end = '\n\n' )

def SYMTAB_print():
    print( 'SYMTAB:' )
    print( '-------------------------------------------------', end = '\n' )
    for i in range( len( SYMTAB_name ) ):
        print( '|\t', SYMTAB_name[i], '\t\t|\t', '{:04X}'.format( SYMTAB_addr[i] ), '\t\t|', sep='' )
    print( '-------------------------------------------------', end = '\n\n' )

def formObjectCode( opcode, operand ):
    return

def formObjectCodeConstant( opcode, operand ):
    return

def isCommentLine( s ):
    if s[0] == '.':
        return True
    else:
        return False

def PASS1( raw, info ):
    """ First Line """
    s = raw.readline().split()
    #print("First line: ", end = '' )
    #print(s)
    if not s:
        print( 'This is a blank file :(' )
        exit(0)
    if s[1] == 'START':             # else case is skipped since declaration has done the task
        info[1] = s[0]
        #print( "Program Name: ", programName, sep = '' )
        startAddr = '0x'
        startAddr = startAddr + s[2]
        info[0] = int( startAddr, 16 )
        #print(  "Starting Address: ", startAddr, sep = '' )
        LOCCTR = int( startAddr, 16 )
        #print(  "LOCCTR: ", startAddr, sep = '' )
    else:
        print( 'No START in the first line' )

    ########## DONE ##########

    """ Middle Lines """
    while True:
        s = raw.readline().split()
        #print( "New line: ", end='' )
        #print(s)
        if len(s) > 1:
            if s[0] == 'END':
                break
        if isCommentLine(s) == False:
            # ", X" case
            if len(s) > 1:
                if s[-2][-1] == ',' and s[-1] == 'X':
                    s[-2] = s[-2] + 'X'
                    s.pop(-1)

            # Label, format s into length-3 list
            if len(s) == 3:
                if s[0] in SYMTAB_name:
                    print( 'Error: Duplicate Symbol Declaration: ', s[0] )
                    exit(-1)
                else:
                    SYMTAB_name.append( s[0] )
                    SYMTAB_addr.append( LOCCTR )
            elif len(s) == 2:
                s.insert( 0, "" )
            elif s[0] != 'RSUB':
                print( 'Error in this statement: ', s )
                exit(-1)

            # Modify LOCCTR
            if s[0] != 'RSUB':
                op = ""
                isFormat4 = 0
                if s[1][0] == '+':
                    op = s[1][1:]
                    isFormat4 = 1
                else:
                    op = s[1]

            if op == 'BASE':
                continue
            elif op in OPTAB_name:
                if op == 'CLEAR' or op == 'TIXR' or op == 'COMPR':
                    LOCCTR += 2
                elif isFormat4 == 1:
                    LOCCTR += 4
                else:
                    LOCCTR += 3
            elif s[1] == 'WORD':
                LOCCTR += 3
            elif s[1] == 'BYTE':
                if s[2][0] == 'C':
                    LOCCTR += ( len(s[2]) - 3 )
                elif s[2][0] == 'X':
                    LOCCTR += ( ( len(s[2]) - 3 ) // 2 )
            elif s[1] == 'RESW':
                LOCCTR += 3 * int( s[2] )
            elif s[1] == 'RESB':
                LOCCTR += int( s[2] )
            else:
                print( 'Error: ', s[1], ' is not a legal OPCODE', sep='', end='\n' )
                exit(-1)
            #print( 'LOCCTR: ', hex( LOCCTR ), sep='' )
    info[2] = LOCCTR - info[0]
    return

def PASS2( raw, info ):
    objCode = open( "objCode.txt", "w" )

    """ First Line """
    s = raw.readline().split()
    if not s:
        print( 'This is a blank file :(' )
        exit(0)
    if s[1] == 'START':             # else case is skipped since declaration has done the task
        """ Header """
        HRecord = 'H{:6s}{:06X}{:06X}\n'.format( info[1], info[0], info[2] )
        #HRecord = "H" + info[1] + info[0] + info[2]   # Format the last two parameter is required
        objCode.write( HRecord )

#    TRecord = "T" + str( LOCCTR ) + "00"    # how to write starting addr and length

#    """ Middle Lines """
#    while True:
#        s = raw.readline().split()
#        if s[1] == 'END':
#            break
#        if """ This is not a comment line """:
#            # ", X" case
#            if s[-2][-1] == ',' and s[-1] == 'X':
#                s[-2] = s[-2] + 'X'
#                s.pop(-1)
#
#            # Format s into length-3 list
#            if len(s) == 2:
#                s.insert( 0, "" )
#
#            if """ s[1] in OPTAB """ :
#                formObjectCode( s[1], s[2] )
#            elif s[1] == 'BYTE' or s[1] == 'WORD':
#                """ Convert Constant to ObjectCode """
#                formObjectCodeConstant( s[1], s[2] )
#
#            # Over text record range
#            if """ It's time to create a new T record """:
#                objCode.write( TRecord )
#                TRecord = "T" + str( LOCCTR ) + "00"    # how to write starting addr and length
#            
#
    #ERecord = "E" + str( startAddr ) + '\n'
    ERecord = 'E{:06X}\n'.format( info[0] )
    objCode.write( ERecord )

    objCode.close()
    return

def main():
    # Variables I need
    OPTAB_init()
    info = []   # startAddr, programName, ProgramLength
    startAddr = 0
    info.append( startAddr )
    programName = ""
    info.append( programName )
    LOCCTR = 0
    ProgramLength = 0
    info.append( ProgramLength )

    asmFile = sys.argv[1]
    raw = open( asmFile, 'r' )

    PASS1( raw, info )

    print( '****** PASS1 end ******')
    print( 'Program Name  : ', info[1], sep='' )
    print( 'Program Length: ', hex( info[2] ), sep='', end='\n\n' )

    """ Test: OP table and Symbol Table """
    OPTAB_print()
    SYMTAB_print()

    raw.seek(0)     # Back to the file beginning
    
    PASS2( raw, info )

    raw.close()
    
if __name__ == "__main__":
    main()

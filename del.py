# if (db.query(models.User).count() == 0):
# if (request.password == "Pass@1234"):

#     admin_user = models.User(username=request.username, created_by=request.username,
#                              password=hashing.Hash.bcrypt(request.password), is_admin=True)
#     db.add(admin_user)
#     db.commit()
#     db.refresh(admin_user)
#     access_token = tokens.create_access_token(data={"user": {
#         "username": request.username,"isAdmin": True}})

#     return {"access_token": access_token, "token_type": "bearer"}

# else:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail="Incorrect Passwords")

# else:


# delete html code goes below
# <section class="footer">
#       <div class="col footer-about">
#         <a href="" class="brand-lg"> brands<span>U</span>rl </a>
#         <p>
#           BrandURL is a short URL service that offers custom domain branding,
#           password protection, link expiration, and tracking features. BrandURL
#           provides detailed analytics to track clicks, location, and device
#           type.
#         </p>
#       </div>

#       <div class="col footer-company">
#         <h4>Company</h4>
#         <ul>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer">
#               Teams
#             </a>
#           </li>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer">
#               Supports</a
#             >
#           </li>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer"> FAQ</a>
#           </li>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer"
#               >Customer Testimonial</a
#             >
#           </li>
#         </ul>
#       </div>
#       <div class="col footer-resources">
#         <h4>Usefull Links</h4>
#         <ul>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer">
#               Privacy Policy</a
#             >
#           </li>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer">
#               Terms & Conditions</a
#             >
#           </li>
#           <li>
#             <a href="http://" target="_blank" rel="noopener noreferrer">
#               Refunds</a
#             >
#           </li>
#         </ul>
#       </div>
#     </section>

# if not len(request.username) >= 8:
#     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                         detail=f"{request.username} length must be gretter than 8 character.")
# else:
# else:
#     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                         detail=f"{request.username} already exists.")
# if val_user.count() == 0:
#     new_user = models.User(fullname="Shreeganesh", email_address=request.email_address, created_by=request.email_address,
#                             password=hashing.Hash.bcrypt(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     access_token = tokens.create_access_token(data={"user": {
#         "username": request.username, "email_address": request.email_address, "isAdmin": True}})

#     return {"access_token": access_token, "token_type": "bearer"}

# else:

# app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @router.get('/verifyemail/{verification_code}')
# def VerifyEmail(verification_code: str, db: Session = Depends(get_db)):
#     result = db.query(models.User).filter(
#         models.User.verification_code == verification_code)

#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code')
#     else:
#         result.update({"is_active": True, "verification_code": None})
#         db.commit()

#     return {"Account verified successfully!"}
# print("Total_visit_count",click_count_update.click_count)